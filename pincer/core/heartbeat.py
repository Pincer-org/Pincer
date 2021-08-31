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
from asyncio import sleep
from typing import Optional

from websockets.legacy.client import WebSocketClientProtocol

from pincer import __package__
from pincer.core.dispatch import GatewayDispatch
from pincer.exceptions import HeartbeatError


log = logging.getLogger(__package__)


class Heartbeat:
    __heartbeat: float = 0
    __sequence: Optional[int] = None

    @staticmethod
    async def __send(socket: WebSocketClientProtocol):
        """
        Sends a heartbeat to the API gateway.
        """
        log.debug(f"Sending heartbeat (seq: {Heartbeat.__sequence})")
        await socket.send(str(GatewayDispatch(1, Heartbeat.__sequence)))

    @staticmethod
    def get() -> float:
        """
        Get the current heartbeat.

        :return:
            The current heartbeat of the client.
            Default is 0 (client has not initialized the heartbeat yet.)

        """
        return Heartbeat.__heartbeat

    @staticmethod
    async def handle_hello(
        socket: WebSocketClientProtocol,
        payload: GatewayDispatch
    ):
        """
        Handshake between the discord API and the client.
        Retrieve the heartbeat for maintaining a connection.
        """
        log.debug("Handling initial discord hello websocket message.")
        Heartbeat.__heartbeat = payload.data.get("heartbeat_interval")

        if not Heartbeat.__heartbeat:
            log.error(
                "No `heartbeat_interval` is present. Has the API changed? "
                f"(payload: {payload})"
            )

            raise HeartbeatError(
                "Discord hello is missing `heartbeat_interval` in payload."
                "Because of this the client can not maintain a connection. "
                "Check logging for more information."
            )

        Heartbeat.__heartbeat /= 1000

        log.debug(
            f"Maintaining a connection with heartbeat: {Heartbeat.__heartbeat}"
        )

        if Heartbeat.__sequence:
            await socket.send(
                str(
                    GatewayDispatch(
                        6,
                        Heartbeat.__sequence,
                        seq=Heartbeat.__sequence
                    )
                )
            )

        else:
            await Heartbeat.__send(socket)

    @staticmethod
    async def handle_heartbeat(socket: WebSocketClientProtocol, _):
        """
        Handles a heartbeat, which means that it rests and then sends a new
        heartbeat.
        """

        logging.debug(f"Resting heart for {Heartbeat.__heartbeat}s")
        await sleep(Heartbeat.__heartbeat)
        await Heartbeat.__send(socket)

    @staticmethod
    def update_sequence(seq: int):
        """
        Update the heartbeat sequence.

        :param seq:
            The new heartbeat sequence to be updated with.
        """
        log.debug("Updating heartbeat sequence...")
        Heartbeat.__sequence = seq


handle_hello = Heartbeat.handle_hello
handle_heartbeat = Heartbeat.handle_heartbeat
update_sequence = Heartbeat.update_sequence

__all__ = (handle_hello, handle_heartbeat, update_sequence)
