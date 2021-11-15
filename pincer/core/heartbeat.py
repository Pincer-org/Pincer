# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from asyncio import sleep
from typing import TYPE_CHECKING

from websockets.exceptions import ConnectionClosedOK

from . import __package__
from ..core.dispatch import GatewayDispatch
from ..exceptions import HeartbeatError

if TYPE_CHECKING:
    from typing import Optional

    from websockets.legacy.client import WebSocketClientProtocol


_log = logging.getLogger(__package__)


class Heartbeat:
    """The heartbeat of the websocket connection.

    This is what lets the server and client know that they are still
    both online and properly connected.
    """
    __heartbeat: float = 0
    __sequence: Optional[int] = None

    @classmethod
    async def __send(cls, socket: WebSocketClientProtocol):
        """|Coro|
        Sends a heartbeat to the API gateway.

        Parameters
        ----------
        socket : :class:`~ws:websockets.legacy.client.WebSocketClientProtocol`
            The socket to send the heartbeat to.
        """
        _log.debug("Sending heartbeat (seq: %s)", str(cls.__sequence))
        try:
            await socket.send(str(GatewayDispatch(1, cls.__sequence)))
        except ConnectionClosedOK:
            _log.error(
                "Sending heartbeat failed. Ignoring failure... "
                "Client should automatically resolve this issue. "
                "If a crash occurs please create an issue on our github! "
                "(https://github.com/Pincer-org/Pincer)"
            )

    @classmethod
    def get(cls) -> float:
        """Get the current heartbeat.

        Returns
        -------
        :class:`float`
            The current heartbeat of the client.
            |default| ``0`` (client has not initialized the heartbeat yet.)
        """
        return cls.__heartbeat

    @classmethod
    async def handle_hello(
            cls,
            socket: WebSocketClientProtocol,
            payload: GatewayDispatch
    ):
        """|coro|

        Handshake between the discord API and the client.
        Retrieve the heartbeat for maintaining a connection.

        Parameters
        ----------
        socket : :class:`~ws:websockets.legacy.client.WebSocketClientProtocol`
            The socket to send the heartbeat to.
        payload : :class:`~pincer.core.dispatch.GatewayDispatch`
            The received hello message from the Discord gateway.

        Raises
        ------
        HeartbeatError
            No ``heartbeat_interval`` is present.
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
        """|coro|

        Handles a heartbeat, which means that it rests
        and then sends a new heartbeat.

        Parameters
        ----------
        socket : :class:`~ws:websockets.legacy.client.WebSocketClientProtocol`
            The socket to send the heartbeat to.
        _ :
            Filling param for auto event handling.
        """
        _log.debug("Resting heart for %is", cls.__heartbeat)
        await sleep(cls.__heartbeat)
        await cls.__send(socket)

    @classmethod
    def update_sequence(cls, seq: int):
        """
        Update the heartbeat sequence.

        Parameters
        ----------
        seq : :class:`int`
            The new heartbeat sequence to be updated with.
        """
        _log.debug("Updating heartbeat sequence...")
        cls.__sequence = seq
