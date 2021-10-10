# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

import logging
from asyncio import get_event_loop, AbstractEventLoop, ensure_future
from platform import system
from typing import Dict, Callable, Awaitable, Optional

from websockets import connect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.legacy.client import WebSocketClientProtocol

from . import __package__
from .._config import GatewayConfig
from ..core.dispatch import GatewayDispatch
from ..core.heartbeat import Heartbeat
from ..exceptions import (
    PincerError, InvalidTokenError, UnhandledException,
    _InternalPerformReconnectError, DisallowedIntentsError
)
from ..objects import Intents

Handler = Callable[[WebSocketClientProtocol, GatewayDispatch], Awaitable[None]]
_log = logging.getLogger(__package__)


class Dispatcher:
    """
    The Dispatcher handles all interactions with discord websocket API.
    This also contains the main event loop, and handles the heartbeat.

    Running the dispatcher will create a connection with the
    Discord WebSocket API on behalf of the provided token.

    This token must be a bot token.
    (Which can be found on
    `<https://discord.com/developers/applications/<bot_id>/bot>`_)
    """

    # TODO: Implement compression
    def __init__(
            self, token: str, *,
            handlers: Dict[int, Handler],
            intents: Intents
    ) -> None:
        """
        :param token:
            Bot token for discord's API.

        :param intents:
            Represents the discord bot intents.

        :param handlers:
            A hashmap of coroutines with as key the gateway opcode.

        :raises InvalidTokenError:
            Discord Token length is not 59 characters.
        """

        if len(token) != 59:
            raise InvalidTokenError(
                "Discord Token must have exactly 59 characters."
            )

        self.__token = token
        self.__keep_alive = True
        self.__socket: Optional[WebSocketClientProtocol] = None
        self.__intents = intents

        async def identify_and_handle_hello(
                socket: WebSocketClientProtocol,
                payload: GatewayDispatch
        ):
            """
            Identifies the client to the Discord Websocket API, this
            gets done when the client receives the ``hello`` (opcode 10)
            message from discord. Right after we send our identification
            the heartbeat starts.

            :param socket:
                The current socket, which can be used to interact
                with the Discord API.

            :param payload:
                The received payload from Discord.
            """
            _log.debug("Sending authentication/identification message.")

            await socket.send(self.__hello_socket)
            await Heartbeat.handle_hello(socket, payload)

        async def handle_reconnect(_, payload: GatewayDispatch):
            """
            Closes the client and then reconnects it.
            """
            _log.debug("Reconnecting client...")
            await self.close()

            Heartbeat.update_sequence(payload.seq)
            self.start_loop()

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

    @property
    def intents(self):
        return self.__intents

    @property
    def __hello_socket(self) -> str:
        return str(
            GatewayDispatch(
                2, {
                    "token": self.__token,
                    "intents": self.__intents,
                    "properties": {
                        "$os": system(),
                        "$browser": __package__,
                        "$device": __package__
                    }
                }
            )
        )

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

        :meta public:

        :param socket:
            The current socket, which can be used to interact with
            the Discord API.

        :param payload:
            The received payload from Discord.

        :param loop:
            The current async loop on which the future is bound.
        """
        _log.debug(
            "New event received, checking if handler exists for opcode: %i",
            payload.op
        )

        handler: Handler = self.__dispatch_handlers.get(payload.op)
        all_handler: Handler = self.__dispatch_handlers.get(-1)

        if not handler:
            _log.error(
                "No handler was found for opcode %i, please report this to the "
                "pincer dev team!", payload.op
            )

            if not all_handler:
                raise UnhandledException(f"Unhandled payload: {payload}")

        _log.debug(
            "Event handler found, ensuring async future in current loop."
        )

        def execute_handler(event_handler: Handler):
            if event_handler:
                ensure_future(event_handler(socket, payload), loop=loop)

        execute_handler(handler)
        execute_handler(all_handler)

    async def __dispatcher(self, loop: AbstractEventLoop):
        """
        The main event loop.
        This handles all interactions with the websocket API.

        :meta public:

        :param loop:
            The loop in which the dispatcher is running.
        """
        _log.debug(
            "Establishing websocket connection with `%s`", GatewayConfig.uri()
        )

        async with connect(GatewayConfig.uri()) as socket:
            self.__socket = socket
            _log.debug(
                "Successfully established websocket connection with `%s`",
                GatewayConfig.uri()
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
                        "The connection with `%s` has been broken unexpectedly."
                        " (%i, %s)", GatewayConfig.uri(), exc.code, exc.reason
                    )

                    await self.close()
                    exception = self.__dispatch_errors.get(exc.code)

                    if isinstance(exception, _InternalPerformReconnectError):
                        Heartbeat.update_sequence(0)
                        return self.start_loop()

                    raise exception or UnhandledException(
                        f"Dispatch error ({exc.code}): {exc.reason}"
                    )
                except ConnectionClosedOK:
                    _log.debug("Connection closed successfully.")

    def start_loop(self, *, loop: AbstractEventLoop = None):
        """
        Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client who's token has
        been passed.

        Keyword Arguments:

        :param loop:
            The loop in which the Dispatcher will run. If no loop is
            provided it will get a new one.
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
            "Setting keep_alive to False, this will terminate the heartbeat."
        )

        self.__keep_alive = False
        await self.__socket.close()
