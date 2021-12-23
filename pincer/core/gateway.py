# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

from asyncio import AbstractEventLoop, create_task, get_event_loop
from asyncio.tasks import Task, ensure_future, sleep
from dataclasses import dataclass
from datetime import datetime
import logging
from platform import system
from random import random
from typing import Any, Dict, Callable, Awaitable, Optional, Tuple
from typing import TYPE_CHECKING
from zlib import decompressobj

from aiohttp import ClientSession, WSMsgType, ClientConnectorError

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
    Handler = Callable[[GatewayDispatch], None]

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

        # ClientSession to be used for this Dispatcher
        self.__session = ClientSession()

        # The gateway can be disconnected from Discord. This variable stores if the
        # gateway should send a hello or reconnect.
        self.__should_reconnect: bool = False

        # The squence number for the last recieved payload. This is used reconnecting.
        self.__sequence_number: int = 0

        """Code for handling heartbeat"""
        # The heartbeat task
        self.__heartbeat_task: Optional[Task] = None

        # Keeps the Client waiting until the next heartbeat
        self.__wait_for_heartbeat: Optional[Task] = None

        # How long the client should wait between each Heartbeat.
        self.__heartbeat_interval: Optional[int] = None

        # Tracks whether the gateway has recieved an ack (opcode 11) since the last
        # heartbeat.
        #   True: An ack has been recieved
        #   False: No ack has been recieved. Attempt to reconnect with gateway,
        self.__has_recieved_ack: bool = True

        # Session ID recieved from `on_ready` event. It is set in the `on_ready`
        # middleware. This is used reconnecting.
        self.__session_id: Optional[str] = None

    def __del__(self):
        create_task(self.socket.close())

    def append_handlers(self, handlers: Dict[int, Handler]):
        self.__dispatch_handlers = handlers | self.__dispatch_handlers

    async def start_loop(self):
        """Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client whose token has
        been passed.
        """
        while True:
            try:
                self.socket = await self.__session.ws_connect(
                    GatewayConfig.make_uri(self.url)
                )
                break
            except ClientConnectorError:
                _log.warning(
                    "%s Could not open websocket with Discord."
                    "Retrying in 15 seconds...",
                    self.shard_key
                )
                await sleep(15)

        _log.debug("%s Starting envent loop...", self.shard_key)
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

        _log.debug(
            "%s %s GatewayDispatch with opcode %s recieved",
            self.shard_key,
            datetime.now(),
            payload.op
        )

        if payload.seq is not None and payload.seq >= self.__sequence_number:
            self.__sequence_number = payload.seq
            _log.debug("%s Set squence number to %s", self.shard_key, payload.seq)

        handler = self.__dispatch_handlers.get(payload.op)

        if handler is None:
            raise Exception

        ensure_future(handler(payload))

    async def handle_heartbeat_req(self, payload: GatewayDispatch):
        self.send_next_heartbeat()

    async def handle_reconnect(self, payload: GatewayDispatch):
        _log.debug(
            "%s Requested to reconnect to Discord. Closing session and attemping to"
            "resume...",
            self.shard_key
        )

        await self.socket.close(code=1000)
        self.__should_reconnect = True
        await self.start_loop()

    async def handle_invalid_session(self, payload: GatewayDispatch):
        """
        Attempt to relog on invalid connection
        """
        _log.debug("%s Invalid session, attempting to relog...", self.shard_key)
        self.__should_reconnect = False
        await self.start_loop()

    async def identify_and_handle_hello(self, payload: GatewayDispatch):

        if self.__should_reconnect:
            await self.resume()
            return

        await self.send(str(
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
        ))
        self.__heartbeat_interval = payload.data["heartbeat_interval"]

        self.start_heartbeat()

    async def handle_heartbeat(self, payload: GatewayDispatch):
        self.__has_recieved_ack = True

    async def send(self, payload: str):
        safe_payload = payload.replace(self.token, "%s..." % self.token[:10])

        if self.__session_id:
            safe_payload = safe_payload.replace(
                self.__session_id, "%s..." % self.__session_id[:4]
            )

        _log.debug(
            "%s Sending payload: %s",
            self.shard_key,
            safe_payload
        )

        if self.socket.closed:
            _log.debug(
                "%s Socket is closing. Payload not sent.",
                self.shard_key
            )
            return

        await self.socket.send_str(payload)

    async def resume(self):
        _log.debug(
            "%s Disconnected from discord. Attempting to reconnect \U0001f480",
            self.shard_key
        )

        res = str(GatewayDispatch(
            6,
            {
                "token": self.token,
                "session_id": self.session_id,
                "seq": self.__sequence_number
            }
        ))

        await self.send(res)

    def set_session_id(self, _id: str):
        self.__session_id = _id

    """Code for handling Heartbeat"""

    def start_heartbeat(self):
        if not self.__heartbeat_task or self.__heartbeat_task.cancelled():
            self.__heartbeat_task = ensure_future(self.__heartbeat_loop())

    def stop_heartbeat(self):
        self.__heartbeat_task.cancel()

    def send_next_heartbeat(self):
        self.__wait_for_heartbeat.cancel()

    async def __heartbeat_loop(self):

        _log.debug("%s Starting heartbeat loop...", self.shard_key)
        # When waiting for first heartbeat, there hasn't been an ack recieved yet.
        # Set to true so the ack recieved check doesn't fail.
        self.__has_recieved_ack = True

        jitter = random()

        while True:
            duration = self.__heartbeat_interval * jitter

            _log.debug(
                "%s %s sending heartbeat in %sms",
                self.shard_key, datetime.now(),
                duration
            )

            self.__wait_for_heartbeat = create_task(
                sleep(duration / 1000)
            )

            jitter = 1

            await self.__wait_for_heartbeat

            if not self.__has_recieved_ack:
                _log.debug(
                    "%s %s ack not recieved. Closing socket with close code 1001.",
                    datetime.now(),
                    self.shard_key
                )
                await self.socket.close(code=1001)
                self.__should_reconnect = True
                ensure_future(self.start_loop())
                self.stop_heartbeat()
                return

            self.__has_recieved_ack = False
            await self.send(str(GatewayDispatch(1, data=self.__sequence_number)))
            _log.debug("%s sent heartbeat", self.shard_key)
