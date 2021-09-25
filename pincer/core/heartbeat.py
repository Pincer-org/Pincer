# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from asyncio import sleep
from typing import Optional

from websockets.legacy.client import WebSocketClientProtocol

from . import __package__
from ..core.dispatch import GatewayDispatch
from ..exceptions import HeartbeatError

_log = logging.getLogger(__package__)


class Heartbeat:
    """
    The heartbeat of the websocket connection.

    This is what lets the server and client know that they are still
        both online and properly connected.
    """
    __heartbeat: float = 0
    __sequence: Optional[int] = None

    @classmethod
    async def __send(cls, socket: WebSocketClientProtocol):
        """
        Sends a heartbeat to the API gateway.
        :meta public:

        :param socket:
            The socket to send the heartbeat to.
        """
        _log.debug("Sending heartbeat (seq: %s)", str(cls.__sequence))
        await socket.send(str(GatewayDispatch(1, cls.__sequence)))

    @classmethod
    def get(cls) -> float:
        """
        Get the current heartbeat.

        :return:
            The current heartbeat of the client.
            Default is 0 (client has not initialized the heartbeat yet.)
        """
        return cls.__heartbeat

    @classmethod
    async def handle_hello(
            cls,
            socket: WebSocketClientProtocol,
            payload: GatewayDispatch
    ):
        """
        Handshake between the discord API and the client.
        Retrieve the heartbeat for maintaining a connection.

        :param socket:
            The socket to send the heartbeat to.

        :param payload:
            The received hello message from the Discord gateway.
        """
        _log.debug("Handling initial discord hello websocket message.")
        cls.__heartbeat = payload.data.get("heartbeat_interval")

        if not cls.__heartbeat:
            _log.error(
                "No `heartbeat_interval` is present. Has the API changed? "
                "(payload: %s)", payload
            )

            raise HeartbeatError(
                "Discord hello is missing `heartbeat_interval` in payload."
                "Because of this the client can not maintain a connection. "
                "Check logging for more information."
            )

        cls.__heartbeat /= 1000

        _log.debug(
            "Maintaining a connection with heartbeat: %s", cls.__heartbeat
        )

        if Heartbeat.__sequence:
            await socket.send(
                str(GatewayDispatch(6, cls.__sequence, seq=cls.__sequence))
            )

        else:
            await cls.__send(socket)

    @classmethod
    async def handle_heartbeat(cls, socket: WebSocketClientProtocol, _):
        """
        Handles a heartbeat, which means that it rests
        and then sends a new heartbeat.

        :param socket:
            The socket to send the heartbeat to.

        :param _:
            Filling param for auto event handling.
        """

        _log.debug("Resting heart for %is", cls.__heartbeat)
        await sleep(cls.__heartbeat)
        await cls.__send(socket)

    @classmethod
    def update_sequence(cls, seq: int):
        """
        Update the heartbeat sequence.

        :param seq:
            The new heartbeat sequence to be updated with.
        """
        _log.debug("Updating heartbeat sequence...")
        cls.__sequence = seq
