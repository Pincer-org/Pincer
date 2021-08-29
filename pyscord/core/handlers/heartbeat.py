# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pyscord
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

from asyncio import sleep
from typing import Optional

from websockets.legacy.client import WebSocketClientProtocol

from pyscord.core.dispatch import GatewayDispatch

heartbeat: float = 0
sequence: Optional[int] = None


async def __send_heartbeat(socket: WebSocketClientProtocol):
    # TODO: Fix docs
    # TODO: Implement logging
    await socket.send(str(GatewayDispatch(1, sequence)))


async def handle_hello(socket: WebSocketClientProtocol,
                       payload: GatewayDispatch):
    # TODO: Fix docs
    # TODO: Implement logging
    global heartbeat, sequence
    heartbeat = payload.data.get("heartbeat_interval")

    if not heartbeat:
        # TODO: Throw invalid heartbeat exception if no heartbeat is present.
        return

    heartbeat /= 1000

    await __send_heartbeat(socket)


async def handle_heartbeat(socket: WebSocketClientProtocol, _):
    # TODO: Fix docs
    # TODO: Implement logging
    await sleep(heartbeat)
    await __send_heartbeat(socket)
