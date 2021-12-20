# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

from asyncio import AbstractEventLoop, create_task, get_event_loop
from dataclasses import dataclass
import logging
from platform import system
from typing import Any, Dict, Callable, Awaitable, Optional, Tuple
from typing import TYPE_CHECKING
from zlib import decompressobj

from aiohttp import ClientSession, WSMsgType

from . import __package__
from ..utils.api_object import APIObject
from .._config import GatewayConfig
from ..core.dispatch import GatewayDispatch
from ..exceptions import (
    PincerError, InvalidTokenError, UnhandledException,
    _InternalPerformReconnectError, DisallowedIntentsError
)

if TYPE_CHECKING:
    from ..objects.app.intents import Intents

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
inflator = decompressobj()

_log = logging.getLogger(__package__)


@dataclass
class Gateway(APIObject):
    url: str
    shards: int
    session_start_limit: SessionStartLimit


@dataclass
class SessionStartLimit(APIObject):
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


class Dispatcher:
    """The Dispatcher handles all interactions with the Discord Websocket API.
    This also contains the main event loop, and handles the heartbeat.

    Running the dispatcher will create a connection with the
    Discord Websocket API on behalf of the provided token.

    This token must be a bot token.
    (Which can be found on
    `<https://discord.com/developers/applications/>`_)
    """

    def __init__(
            self,
            token: str, *,
            intents: Intents,
            url: str,
            shard: int,
            num_shards: int
    ) -> None:
        if len(token) != 59:
            raise InvalidTokenError(
                "Discord Token must have exactly 59 characters."
            )

        self.token = token
        self.intents = intents
        self.url = url
        self.shard = shard
        self.num_shards = num_shards
        self.shard_key = [shard, num_shards]

        self.__dispatch_handlers: Dict[int, Handler] = {
            1: self.handle_heartbeat_req,
            7: self.handle_reconnect,
            9: self.handle_invalid_session,
            10: self.identify_and_handle_hello,
            11: self.handle_heartbeat
        }

        self.__dispatch_errors: Dict[int, PincerError] = {
            1006: _InternalPerformReconnectError(),
            4000: _InternalPerformReconnectError(),
            4004: InvalidTokenError(),
            4007: _InternalPerformReconnectError(),
            4009: _InternalPerformReconnectError(),
            4014: DisallowedIntentsError()
        }

        self.__heartbeat_interval = None

    def __del__(self):
        create_task(self.socket.close())

    def append_handlers(self, handlers: Dict[int, Handler]):
        self.__dispatch_handlers = handlers | self.__dispatch_handlers

    async def start_loop(self):
        """Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client whose token has
        been passed.
        """

        self.__session = ClientSession()
        self.socket = await self.__session.ws_connect(GatewayConfig.make_uri(self.url))
        await self.event_loop()

    async def event_loop(self):
        async for msg in self.socket:
            if msg.type == WSMsgType.TEXT:
                await self.handle_data(msg.data)
            elif msg.type == WSMsgType.BINARY:

                # Method used to decompress payload copied from docs
                # https://discord.com/developers/docs/topics/gateway#transport-compression-transport-compression-example
                if len(msg.data) < 4 or msg.data[-4:] != ZLIB_SUFFIX:
                    return

                await self.handle_data(inflator.decompress(msg.data))

    async def handle_data(self, data: Dict[Any]):
        payload = GatewayDispatch.from_string(data)

        handler = self.__dispatch_handlers.get(payload.op)

        if handler is None:
            raise Exception

        await handler(payload)

    @property
    def __hello_socket(self) -> str:
        return str(
            GatewayDispatch(
                2, {
                    "token": self.token,
                    "intents": self.intents,
                    "properties": {
                        "$os": system(),
                        "$browser": __package__,
                        "$device": __package__
                    },
                    "compress": GatewayConfig.compressed(),
                    "shard": self.shard_key
                }
            )
        )

    async def send(self, payload: str):
        await self.socket.send_str(payload)

    async def handle_heartbeat_req(self, payload: GatewayDispatch):
        pass

    async def handle_reconnect(self, payload: GatewayDispatch):
        pass

    async def handle_invalid_session(self, payload: GatewayDispatch):
        pass

    async def identify_and_handle_hello(self, payload: GatewayDispatch):
        self.__heartbeat_interval = payload.data["heartbeat_interval"]
        await self.send(self.__hello_socket)

    async def handle_heartbeat(self, payload: GatewayDispatch):
        pass
