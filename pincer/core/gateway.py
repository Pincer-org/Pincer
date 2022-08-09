# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from __future__ import annotations

from asyncio import create_task, Task, ensure_future, sleep
from dataclasses import dataclass
from datetime import datetime
from itertools import repeat, count, chain
import logging
from platform import system
from random import random
from typing import TYPE_CHECKING, Any, Dict, Callable, Optional
from zlib import decompressobj

from aiohttp import (
    ClientSession,
    WSMsgType,
    ClientConnectorError,
    ClientWebSocketResponse,
)

from . import __package__
from ..utils.api_object import APIObject
from .._config import GatewayConfig
from ..core.dispatch import GatewayDispatch
from ..exceptions import (
    InvalidTokenError,
    GatewayConnectionError,
    GatewayError,
    UnhandledException,
)

if TYPE_CHECKING:
    from ..objects.app.intents import Intents

    Handler = Callable[[GatewayDispatch], None]

_log = logging.getLogger(__package__)

ZLIB_SUFFIX = b"\x00\x00\xff\xff"
inflator = decompressobj()


@dataclass
class SessionStartLimit(APIObject):
    """Session start limit info returned from the `gateway/bot` endpoint"""

    total: int
    remaining: int
    reset_after: int
    max_concurrency: int


@dataclass
class GatewayInfo(APIObject):
    """Gateway info returned from the `gateway/bot` endpoint"""

    url: str
    shards: int
    session_start_limit: SessionStartLimit


class Gateway:
    """The Gateway handles all interactions with the Discord Websocket API.
    This also contains the main event loop, and handles the heartbeat.

    Running the Gateway will create a connection with the
    Discord Websocket API on behalf of the provided token.

    This token must be a bot token.
    (Which can be found on
    `<https://discord.com/developers/applications/>`_)

    Parameters
    ----------
    token : str.
        The token for this bot
    intents : :class:`~pincer.objects.app.intents.Intents`
        The intents to use. More information can be found at
        `<https://discord.com/developers/docs/topics/gateway#gateway-intents>`_.
    url : str
        The gateway url.
    shard : int
        The ID of the shard to run.
    num_shards : int
        Number used to route traffic to the current. This should usually be the total
        number of shards that will be run. More information at
        `<https://discord.com/developers/docs/topics/gateway#sharding>`_.
    """

    def __init__(
        self,
        token: str,
        *,
        intents: Intents,
        url: str,
        shard: int,
        num_shards: int,
    ) -> None:
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
            11: self.handle_heartbeat,
        }

        # 4000 and 4009 are not included. The client will reconnect when receiving
        # either. Code 4000 is also used for internal disconnects that will lead to a
        # reconnect.
        self.__close_codes: Dict[int, GatewayError] = {
            4001: GatewayError("Invalid opcode was sent"),
            4002: GatewayError("Invalid payload was sent."),
            4003: GatewayError("Payload was sent prior to identifying"),
            4004: GatewayError("Token is not valid"),
            4005: GatewayError(
                "Authentication was sent after client already authenticated"
            ),
            4007: GatewayError(
                "Invalid sequence sent when starting new session"
            ),
            4008: GatewayError("Client was rate limited"),
            4010: GatewayError("Invalid shard"),
            4011: GatewayError("Sharding required"),
            4012: GatewayError("Invalid API version"),
            4013: GatewayError("Invalid intents"),
            4014: GatewayError("Disallowed intents"),
        }

        # ClientSession to be used for this Dispatcher
        self.__session: Optional[ClientSession] = None

        # This type `_WSRequestContextManager` isn't exposed by aiohttp.
        # `ClientWebSocketResponse` is a parent class.
        self.__socket: Optional[ClientWebSocketResponse] = None

        # Buffer used to store information in transport compression.
        self.__buffer = bytearray()

        # The gateway can be disconnected from Discord. This variable stores if the
        # gateway should send a hello or reconnect.
        self.__should_resume: bool = False

        # The sequence number for the last received payload. This is used reconnecting.
        self.__sequence_number: int = 0

        # The heartbeat task
        self.__heartbeat_task: Optional[Task] = None

        # Keeps the Client waiting until the next heartbeat
        self.__wait_for_heartbeat: Optional[Task] = None

        # How long the client should wait between each Heartbeat.
        self.__heartbeat_interval: Optional[int] = None

        # Tracks whether the gateway has received an ack (opcode 11) since the last
        # heartbeat.
        #   True: An ack has been received
        #   False: No ack has been received. Attempt to reconnect with gateway,
        self.__has_received_ack: bool = True

        # Session ID received from `on_ready` event. It is set in the `on_ready`
        # middleware. This is used reconnecting.
        self.__session_id: Optional[str] = None

    def __del__(self):
        """Delete method ensures all connections are closed"""
        if self.__socket:
            create_task(self.__socket.close())
        if self.__session:
            create_task(self.__session.close())

    async def init_session(self):
        """|coro|
        Crates the ClientSession. ALWAYS run this function right after initializing
        a Gateway.
        """
        self.__session = ClientSession()

    def append_handlers(self, handlers: Dict[int, Handler]):
        """The Client that uses the handler can append their own methods. The gateway
        will run those methods when the specified opcode is received.
        """
        self.__dispatch_handlers = {**self.__dispatch_handlers, **handlers}

    def set_session_id(self, _id: str):
        """Session id is private for consistency"""
        self.__session_id = _id

    def decompress_msg(self, msg: bytes) -> Optional[str]:
        if GatewayConfig.compression == "zlib-payload":
            return inflator.decompress(msg)

        if GatewayConfig.compression == "zlib-stream":
            self.__buffer.extend(msg)

            if len(self.__buffer) < 4 or self.__buffer[-4:] != ZLIB_SUFFIX:
                return None

            msg = inflator.decompress(msg)
            self.__buffer = bytearray()
            return msg

        return None

    async def start_loop(self):
        """|coro|
        Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client whose token has
        been passed.
        """
        for _try in count():
            try:
                self.__socket = await self.__session.ws_connect(
                    GatewayConfig.make_uri(self.url)
                )
                break
            except ClientConnectorError as e:
                if _try > GatewayConfig.MAX_RETRIES:
                    raise GatewayConnectionError from e

                _log.warning(
                    "%s Could not open websocket with Discord."
                    " Retrying in 15 seconds...",
                    self.shard_key,
                )
                await sleep(15)

        _log.debug("%s Starting event loop...", self.shard_key)
        await self.event_loop()

    async def event_loop(self):
        """|coro|
        Handles receiving messages and decompressing them if needed
        """
        async for msg in self.__socket:
            if msg.type == WSMsgType.TEXT:
                await self.handle_data(msg.data)
            elif msg.type == WSMsgType.BINARY:
                # Message from transport compression that isn't complete returns None
                data = self.decompress_msg(msg.data)
                if data:
                    await self.handle_data(data)
            elif msg.type == WSMsgType.ERROR:
                raise GatewayError from self.__socket.exception()

        # The loop is broken when the gateway stops receiving messages.
        # The "error" op codes are in `self.__close_codes`. The rest of the
        # close codes are unknown issues (such as an unintended disconnect) so the
        # client should reconnect to the gateway.
        err = self.__close_codes.get(self.__socket.close_code)

        if err:
            raise err

        _log.debug(
            "%s Disconnected from Gateway due without any errors. Reconnecting.",
            self.shard_key,
        )
        # ensure_future prevents a stack overflow
        ensure_future(self.start_loop())

    async def handle_data(self, data: Dict[Any]):
        """|coro|
        Method is run when a payload is received from the gateway.
        The message is expected to already have been decompressed.
        Handling the opcode is forked to the background, so they aren't blocking.
        """
        payload = GatewayDispatch.from_string(data)

        # Op code -1 is activated on all payloads
        op_negative_one = self.__dispatch_handlers.get(-1)
        if op_negative_one:
            ensure_future(op_negative_one(payload))

        _log.debug(
            "%s %s GatewayDispatch with opcode %s received",
            self.shard_key,
            datetime.now(),
            payload.op,
        )

        # Many events are sent with a `null` sequence. This sequence should not
        # be tracked.
        if payload.seq is not None:
            self.__sequence_number = payload.seq
            _log.debug(
                "%s Set sequence number to %s", self.shard_key, payload.seq
            )

        handler = self.__dispatch_handlers.get(payload.op)

        if handler is None:
            raise UnhandledException(
                f"Opcode {payload.op} does not have a handler"
            )

        ensure_future(handler(payload))

    async def handle_heartbeat_req(self, payload: GatewayDispatch):
        """|coro|
        Opcode 1 - Instantly send a heartbeat.
        """
        self.send_next_heartbeat()

    async def handle_reconnect(self, payload: GatewayDispatch):
        """|coro|
        Opcode 7 - Reconnect and resume immediately.
        """
        _log.debug(
            "%s Requested to reconnect to Discord. Closing session and attempting to"
            " resume...",
            self.shard_key,
        )

        self.__should_resume = True
        await self.__socket.close()

    async def handle_invalid_session(self, payload: GatewayDispatch):
        """|coro|
        Opcode 9 - Invalid connection
        Attempt to relog. This is probably because the session was already invalidated
        when we tried to reconnect.
        """

        _log.debug(
            "%s Invalid session, attempting to %s...",
            self.shard_key,
            "reconnect" if payload.data else "relog",
        )

        self.__should_resume = payload.data
        self.stop_heartbeat()
        await self.__socket.close()

    async def identify_and_handle_hello(self, payload: GatewayDispatch):
        """|coro|
        Opcode 10 - Hello there general kenobi
        Runs when we connect to the gateway for the first time and every time after.
        If the client thinks it should reconnect, the opcode 6 resume payload is sent
        instead of the opcode 2 hello payload. A new session is only started after a
        reconnect if pcode 9 is received.

        Successful reconnects are handled in the `resumed` middleware.
        """
        if self.__should_resume:
            _log.debug("%s Resuming connection with Discord", self.shard_key)

            await self.send(
                str(
                    GatewayDispatch(
                        6,
                        {
                            "token": self.token,
                            "session_id": self.__session_id,
                            "seq": self.__sequence_number,
                        },
                    )
                )
            )
            return

        await self.send(
            str(
                GatewayDispatch(
                    2,
                    {
                        "token": self.token,
                        "intents": self.intents,
                        "properties": {
                            "$os": system(),
                            "$browser": __package__,
                            "$device": __package__,
                        },
                        "compress": GatewayConfig.compressed(),
                        "shard": self.shard_key,
                    },
                )
            )
        )
        self.__heartbeat_interval = payload.data["heartbeat_interval"]

        self.start_heartbeat()

    async def handle_heartbeat(self, payload: GatewayDispatch):
        """|coro|
        Opcode 11 - Heartbeat
        Track that the heartbeat has been received using shared state (Rustaceans would
        be very mad)
        """
        self.__has_received_ack = True

    async def send(self, payload: str):
        """|coro|
        Send a string object to the payload. Most of this method is just logging,
        the last line is the only one that matters for functionality.
        """
        safe_payload = payload.replace(self.token, "%s..." % self.token[:10])

        if self.__session_id:
            safe_payload = safe_payload.replace(
                self.__session_id, "%s..." % self.__session_id[:4]
            )

        _log.debug("%s Sending payload: %s", self.shard_key, safe_payload)

        if self.__socket.closed:
            _log.debug(
                "%s Socket is closing. Payload not sent.", self.shard_key
            )
            return

        await self.__socket.send_str(payload)

    def start_heartbeat(self):
        """
        Starts the heartbeat if it is not already running.
        """
        if not self.__heartbeat_task or self.__heartbeat_task.cancelled():
            self.__heartbeat_task = ensure_future(self.__heartbeat_loop())

    def stop_heartbeat(self):
        self.__heartbeat_task.cancel()

    def send_next_heartbeat(self):
        """
        It is expected to always be waiting for a heartbeat. By canceling that task,
        a heartbeat can be sent.
        """
        self.__wait_for_heartbeat.cancel()

    async def __heartbeat_loop(self):
        """|coro|
        The heartbeat is responsible for keeping the connection to Discord alive.

        Jitter is only random for the first heartbeat. It should be 1 every other
        heartbeat.
        """
        _log.debug("%s Starting heartbeat loop...", self.shard_key)

        # When waiting for first heartbeat, there hasn't been an ack received yet.
        # Set to true so the ack received check doesn't incorrectly fail.
        self.__has_received_ack = True

        for jitter in chain((random(),), repeat(1)):
            duration = self.__heartbeat_interval * jitter

            _log.debug(
                "%s %s sending heartbeat in %sms",
                self.shard_key,
                datetime.now(),
                duration,
            )

            # Task is needed so waiting can be cancelled by op code 1
            self.__wait_for_heartbeat = create_task(sleep(duration / 1000))

            await self.__wait_for_heartbeat

            if not self.__has_received_ack:
                # Close code is specified to be anything that is not 1000 in the docs.
                _log.debug(
                    "%s %s ack not received. Attempting to reconnect."
                    " Closing socket with close code 4000. \U0001f480",
                    datetime.now(),
                    self.shard_key,
                )
                await self.__socket.close(code=4000)
                self.__should_resume = True
                # A new loop is started in the background while this one is stopped.
                self.stop_heartbeat()
                return

            self.__has_received_ack = False
            await self.send(
                str(GatewayDispatch(1, data=self.__sequence_number))
            )
            _log.debug("%s sent heartbeat", self.shard_key)
