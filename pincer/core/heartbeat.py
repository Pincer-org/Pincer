# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from asyncio import sleep, Task, create_task
from typing import TYPE_CHECKING

from websockets.exceptions import ConnectionClosedOK

from . import __package__
from ..core.dispatch import GatewayDispatch
from ..exceptions import HeartbeatError

if TYPE_CHECKING:
    from typing import Optional

    from websockets.legacy.client import WebSocketClientProtocol

    from .gateway import Dispatcher

_log = logging.getLogger(__package__)


class Heartbeat:
    """The heartbeat of the websocket connection.

    This is what lets the server and client know that they are still
    both online and properly connected.
    """

    def __init__(self, dispatch: Dispatcher) -> None:
        self.dispatcher = dispatch

        self.heartbeat: float = 0
        self.sequence: Optional[int] = None
        self.has_recieved_ack: bool = False
        self.heartbeat_wait_task: Optional[Task] = None

    async def __send(self, socket: WebSocketClientProtocol):
        """|Coro|
        Sends a heartbeat to the API gateway.

        Parameters
        ----------
        socket : :class:`~ws:websockets.legacy.client.WebSocketClientProtocol`
            The socket to send the heartbeat to.
        """
        _log.debug(
            "%s Sending heartbeat (seq: %s)",
            self.dispatcher.shard_key,
            str(self.sequence)
        )
        try:
            await socket.send(str(GatewayDispatch(1, self.sequence)))
        except ConnectionClosedOK:
            _log.error(
                "%s Sending heartbeat failed. Ignoring failure... "
                "Client should automatically resolve this issue. "
                "If a crash occurs please create an issue on our github! "
                "(https://github.com/Pincer-org/Pincer)",
                self.dispatcher.shard_key
            )

    def get(self) -> float:
        """Get the current heartbeat.

        Returns
        -------
        :class:`float`
            The current heartbeat of the client.
            |default| ``0`` (client has not initialized the heartbeat yet.)
        """
        return self.heartbeat

    async def handle_hello(
            self,
            socket: WebSocketClientProtocol,
            payload: GatewayDispatch,
            dispatcher: Dispatcher
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
        :class:`~pincer.exceptions.HeartbeatError`
            No ``heartbeat_interval`` is present.
        """
        _log.debug(
            "%s Handling initial discord hello websocket message.",
            self.dispatcher.shard_key
        )
        self.heartbeat = payload.data.get("heartbeat_interval")

        if not self.heartbeat:
            _log.error(
                "%s No `heartbeat_interval` is present. Has the API changed? "
                "(payload: %s)", self.dispatcher.shard_key, payload
            )

            raise HeartbeatError(
                "Discord hello is missing `heartbeat_interval` in payload."
                "Because of this the client can not maintain a connection. "
                "Check logging for more information."
            )

        self.heartbeat /= 1000

        _log.debug(
            "%s Maintaining a connection with heartbeat: %s",
            self.dispatcher.shard_key,
            self.heartbeat
        )

        if self.sequence:
            await socket.send(
                str(GatewayDispatch(6, self.sequence, seq=self.sequence))
            )

        else:
            await self.__send(socket)

    async def handle_heartbeat(self, socket: WebSocketClientProtocol, _, dispatch: Dispatcher):
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
        _log.debug("%s Resting heart for %is", dispatch.shard_key, self.heartbeat)

        self.heartbeat_wait_task = create_task(sleep(self.heartbeat))
        await self.heartbeat_wait_task
        self.heartbeat_wait_task = None

        await self.__send(socket)

    async def handle_heartbeat_req(
        self,
        _,
        payload: GatewayDispatch,
        dispatch: Dispatcher
    ):
        """|coro|
        Sends a heartbeat without waiting for the next interval
        """

        _log.debug("%s Heartbeat requested by discord", dispatch.shard_key)

        if self.heartbeat_wait_task:
            self.heartbeat_wait_task.cancel()

    def update_sequence(self, seq: int):
        """
        Update the heartbeat sequence.

        Parameters
        ----------
        seq : :class:`int`
            The new heartbeat sequence to be updated with.
        """
        _log.debug("%s Updating heartbeat sequence...", self.dispatcher.shard_key)
        self.sequence = seq
