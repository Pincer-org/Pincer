# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

import logging
from asyncio import AbstractEventLoop, ensure_future, get_event_loop
from platform import system
from typing import Dict, Callable, Awaitable, Optional
from typing import TYPE_CHECKING

import zlib
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

if TYPE_CHECKING:
    from ..objects.app.intents import Intents

ZLIB_SUFFIX = b'\x00\x00\xff\xff'

Handler = Callable[[WebSocketClientProtocol, GatewayDispatch], Awaitable[None]]
_log = logging.getLogger(__package__)


class Dispatcher:
    """The Dispatcher handles all interactions with discord websocket API.
    This also contains the main event loop, and handles the heartbeat.

    Running the dispatcher will create a connection with the
    Discord WebSocket API on behalf of the provided token.

    This token must be a bot token.
    (Which can be found on
    `<https://discord.com/developers/applications/>`_)
    """

    def __init__(
            self, token: str, *,
            handlers: Dict[int, Handler],
            intents: Intents,
            reconnect: bool
    ) -> None:
        if len(token) != 59:
            raise InvalidTokenError(
                "Discord Token must have exactly 59 characters."
            )

        self.__token = token
        self.__keep_alive = True
        self.__has_closed = self.__should_restart = False
        self.__socket: Optional[WebSocketClientProtocol] = None
        self.__intents = intents
        self.__reconnect = reconnect

        async def identify_and_handle_hello(
                socket: WebSocketClientProtocol,
                payload: GatewayDispatch
        ):
            """|coro|

            Identifies the client to the Discord Websocket API, this
            gets done when the client receives the ``hello`` (opcode 10)
            message from discord. Right after we send our identification
            the heartbeat starts.

            Parameters
            ----------
            socket : :class:`~ws:websockets.legacy.client.WebSocketClientProtocol`
                The current socket, which can be used to interact
                with the Discord API.
            payload : :class:`~pincer.core.dispatch.GatewayDispatch`
                The received payload from Discord.
            """  # noqa: E501
            _log.debug("Sending authentication/identification message.")

            await socket.send(self.__hello_socket)
            await Heartbeat.handle_hello(socket, payload)

        async def handle_reconnect(_, payload: GatewayDispatch):
            """|coro|

            Closes the client and then reconnects it.
            """
            _log.debug("Reconnecting client...")
            await self.restart(payload.seq)

        self.__dispatch_handlers: Dict[int, Handler] = {
            **handlers,
            7: handle_reconnect,
            9: handle_reconnect,
            10: identify_and_handle_hello,
            11: Heartbeat.handle_heartbeat
        }

        self.__dispatch_errors: Dict[int, PincerError] = {
            1006: _InternalPerformReconnectError(),
            4000: _InternalPerformReconnectError(),
            4004: InvalidTokenError(),
            4007: _InternalPerformReconnectError(),
            4009: _InternalPerformReconnectError(),
            4014: DisallowedIntentsError()
        }

    @property
    def intents(self):
        """:class:`app.Intents`"""
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
                    },
                    "compress": GatewayConfig.compressed()
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

        :param loop:
            The loop in which the dispatcher is running.
        """
        _log.debug(
            "Establishing websocket connection with `%s`", GatewayConfig.uri()
        )

        async with connect(GatewayConfig.uri()) as socket:
            socket: WebSocketClientProtocol = socket
            self.__socket = socket

            # Removing the limit of the received socket.
            # Having the default limit can cause an issue
            # with first payload of bigger bots.
            socket.max_size = None

            _log.debug(
                "Successfully established websocket connection with `%s`",
                GatewayConfig.uri()
            )

            if GatewayConfig.compression == "zlib-stream":
                # Create an inflator for compressed data as defined in
                # https://discord.com/developers/docs/topics/gateway
                inflator = zlib.decompressobj()

            while self.__keep_alive:
                try:
                    _log.debug("Waiting for new event.")
                    msg = await socket.recv()

                    if msg == "CLOSE":
                        break

                    if isinstance(msg, bytes):
                        if GatewayConfig.compression == "zlib-payload":
                            msg = zlib.decompress(msg)
                        else:
                            buffer = bytearray(msg)

                            while not buffer.endswith(ZLIB_SUFFIX):
                                buffer.extend(await socket.recv())

                            msg = inflator.decompress(buffer).decode('utf-8')

                    await self.__handler_manager(
                        socket,
                        GatewayDispatch.from_string(msg),
                        loop
                    )

                except ConnectionClosedError as exc:
                    _log.debug(
                        "The connection with `%s` has been broken unexpectedly."
                        " (%i, %s)", GatewayConfig.uri(), exc.code, exc.reason
                    )

                    await self.close()
                    exception = self.__dispatch_errors.get(exc.code)

                    if (
                        isinstance(exception, _InternalPerformReconnectError)
                        and self.__reconnect
                    ):
                        _log.debug("Connection closed, reconnecting...")
                        return await self.restart()

                    raise exception or UnhandledException(
                        f"Dispatch error ({exc.code}): {exc.reason}"
                    )
                except ConnectionClosedOK:
                    _log.debug("Connection closed successfully.")
            self.__has_closed = True

    def start_loop(self, *, loop: AbstractEventLoop = None):
        """Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client who's token has
        been passed.

        Parameters
        ----------
        loop : :class:`~asyncio.AbstractEventLoop`
            The loop in which the Dispatcher will run. If no loop is
            provided it will get a new one. |default| :data:`None`
        """
        loop = loop or get_event_loop()
        self.__keep_alive = True
        self.__has_closed = self.__should_restart = False
        loop.run_until_complete(self.__dispatcher(loop))
        if self.__should_restart:
            return self.start_loop(loop=loop)
        loop.close()

    async def restart(self, /, seq: Optional[int] = None):
        """
        Restart the dispatcher.

        Parameters
        ----------
        seq Optional[:class:`int`]
            The sequence number of the last dispatched event.
            If not provided, the dispatcher will restart with no base
            sequence.
        """
        await self.close()
        Heartbeat.update_sequence(seq)
        self.__should_restart = True

    async def close(self):
        """|coro|

        Stop the dispatcher from listening and responding to gateway
        events. This should let the client close on itself.
        """
        if not self.__socket:
            _log.error("Cannot close non existing socket socket connection.")
            raise RuntimeError("Please open the connection before closing.")

        _log.debug("Closing connection...")
        self.__keep_alive = False

        self.__socket.messages.append("CLOSE")
        if waiter := getattr(self.__socket, "_pop_message_waiter", None):
            waiter.cancel()
        await self.__socket.close()
        _log.debug("Successfully closed connection!")
