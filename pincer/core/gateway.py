# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import annotations

import logging
from asyncio import get_event_loop, AbstractEventLoop, ensure_future
from platform import system
from typing import Dict, Callable, Awaitable, Optional

from websockets import connect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol

from pincer import __package__
from pincer._config import GatewayConfig
from pincer.core.dispatch import GatewayDispatch
from pincer.core.heartbeat import Heartbeat
from pincer.exceptions import (
    PincerError, InvalidTokenError, UnhandledException,
    _InternalPerformReconnectError, DisallowedIntentsError
)

Handler = Callable[[WebSocketClientProtocol, GatewayDispatch], Awaitable[None]]
_log = logging.getLogger(__package__)


class Dispatcher:
    """
    The Dispatcher handles all interactions with discord websocket API.
    This also contains the main event loop, and handles the heartbeat.

    Running the dispatcher will create a connection with the
    Discord WebSocket API on behalf of the provided token.

    This token must be a bot token.
    (Which can be found on `/developers/applications/<bot_id>/bot`)
    """

    # TODO: Add intents argument
    def __init__(self, token: str, *, handlers: Dict[int, Handler]) -> None:
        """
        :param token: Bot token for discord's API.
        """

        if len(token) != 59:
            raise InvalidTokenError(
                "Discord Token must have exactly 59 characters."
            )

        self.__token = token
        self.__keep_alive = True
        self.__socket: Optional[WebSocketClientProtocol] = None

        async def identify_and_handle_hello(
                socket: WebSocketClientProtocol,
                payload: GatewayDispatch
        ):
            """
            Identifies the client to the Discord Websocket API, this
            gets done when the client receives the `hello` (opcode 10)
            message from discord. Right after we send our identification
            the heartbeat starts.

            :param socket:
                The current socket, which can be used to interact
                with the Discord API.

            :param payload: The received payload from Discord.
            """
            _log.debug("Sending authentication/identification message.")

            await socket.send(
                str(
                    GatewayDispatch(
                        2, {
                            "token": token,
                            "intents": 0,
                            "properties": {
                                "$os": system(),
                                "$browser": __package__,
                                "$device": __package__
                            }
                        }
                    )
                )
            )

            await Heartbeat.handle_hello(socket, payload)

        async def handle_reconnect(_, payload: GatewayDispatch):
            """
            Closes the client and then reconnects it.
            """
            _log.debug("Reconnecting client...")
            await self.close()

            Heartbeat.update_sequence(payload.seq)
            self.run()

        self.__dispatch_handlers: Dict[int, Handler] = {
            **handlers,
            7: handle_reconnect,
            9: handle_reconnect,
            10: identify_and_handle_hello,
            11: Heartbeat.handle_heartbeat
        }

        self.__dispatch_errors: Dict[int, PincerError] = {
            4000: _InternalPerformReconnectError(),
            4004: InvalidTokenError(),
            4007: _InternalPerformReconnectError(),
            4009: _InternalPerformReconnectError(),
            4014: DisallowedIntentsError()
        }

    async def __handler_manager(
            self,
            socket: WebSocketClientProtocol,
            payload: GatewayDispatch,
            loop: AbstractEventLoop
    ):
        """
        This manages all handles for given OP codes.
        This method gets invoked for every message that is received from
        Discord.

        :param socket:
            The current socket, which can be used to interact
            with the Discord API.
        :param payload: The received payload from Discord.
        :param loop: The current async loop on which the future is bound.
        """
        _log.debug(
            f"New event received, checking if handler exists for opcode: "
            + str(payload.op)
        )

        handler: Handler = self.__dispatch_handlers.get(payload.op)

        if not handler:
            _log.error(
                f"No handler was found for opcode {payload.op}, "
                "please report this to the pincer dev team!"
            )

            raise UnhandledException(f"Unhandled payload: {payload}")

        _log.debug(
            "Event handler found, ensuring async future in current loop.")
        ensure_future(handler(socket, payload), loop=loop)

    async def __dispatcher(self, loop: AbstractEventLoop):
        """
        The main event loop.
        This handles all interactions with the websocket API.
        """
        _log.debug(
            f"Establishing websocket connection with `{GatewayConfig.uri()}`"
        )

        async with connect(GatewayConfig.uri()) as socket:
            self.__socket = socket
            _log.debug(
                "Successfully established websocket connection with "
                f"`{GatewayConfig.uri()}`"
            )

            while self.__keep_alive:
                try:
                    _log.debug("Waiting for new event.")
                    await self.__handler_manager(
                        socket,
                        GatewayDispatch.from_string(await socket.recv()),
                        loop
                    )

                except ConnectionClosedError as exc:
                    _log.debug(
                        f"The connection with `{GatewayConfig.uri()}` "
                        f"has been broken unexpectedly. "
                        f"({exc.code}, {exc.reason})"
                    )

                    await self.close()
                    exception = self.__dispatch_errors.get(exc.code)

                    if isinstance(exception, _InternalPerformReconnectError):
                        Heartbeat.update_sequence(0)
                        await self.close()
                        return self.run()

                    raise exception or UnhandledException(
                        f"Dispatch error ({exc.code}): {exc.reason}"
                    )
                except ConnectionClosedOK:
                    _log.debug("Connection closed successfully.")

    def run(self, loop: AbstractEventLoop = None):
        """
        Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client who's token has
        been passed.
        """
        _log.debug("Starting GatewayDispatcher")
        loop = loop or get_event_loop()
        loop.run_until_complete(self.__dispatcher(loop))
        loop.close()

    async def close(self):
        """
        Stop the dispatcher from listening and responding to gateway
        events. This should let the client close on itself.
        """
        if not self.__socket:
            _log.error("Cannot close non existing socket socket connection.")
            raise RuntimeError("Please open the connection before closing.")

        _log.debug(
            "Setting keep_alive to False, "
            "this will terminate the heartbeat."
        )

        self.__keep_alive = False
        await self.__socket.close(1000)
