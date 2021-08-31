# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import logging
from asyncio import sleep
from typing import Optional

from websockets.legacy.client import WebSocketClientProtocol

from pincer import __package__
from pincer.core.dispatch import GatewayDispatch
from pincer.exceptions import HeartbeatError

heartbeat: float = 0
sequence: Optional[int] = None

log = logging.getLogger(__package__)


def get_heartbeat() -> float:
    """
    Get the current heartbeat.

    :return: The current heartbeat of the client.
            Default is 0 (client has not initialized the heartbeat yet.)

    """
    return heartbeat


async def __send_heartbeat(socket: WebSocketClientProtocol):
    # TODO: Fix docs

    global sequence

    log.debug(f"Sending heartbeat (seq: {sequence})")
    await socket.send(str(GatewayDispatch(1, sequence)))


async def handle_hello(socket: WebSocketClientProtocol,
                       payload: GatewayDispatch):
    # TODO: Fix docs
    global heartbeat

    log.debug("Handling initial discord hello websocket message.")
    heartbeat = payload.data.get("heartbeat_interval")

    if not heartbeat:
        log.error("No `heartbeat_interval` is present. Has the API changed? "
                  f"(payload: {payload})")
        raise HeartbeatError("Discord hello is missing `heartbeat_interval` "
                             "in payload. Because of this the client can not "
                             f"maintain a connection. Check logging for more "
                             f"information.")

    heartbeat /= 1000
    log.debug(f"Maintaining a connection with heartbeat: {heartbeat}")

    if sequence:
        await socket.send(str(GatewayDispatch(6, sequence, seq=sequence)))
    else:
        await __send_heartbeat(socket)


async def handle_heartbeat(socket: WebSocketClientProtocol, _):
    # TODO: Fix docs
    global heartbeat

    logging.debug(f"Resting heart for {heartbeat}s")
    await sleep(heartbeat)
    await __send_heartbeat(socket)


def update_sequence(seq: int):
    # TODO: Fix docs
    global sequence
    log.debug("Updating heartbeat sequence...")
    sequence = seq
