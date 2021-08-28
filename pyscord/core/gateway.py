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

from asyncio import get_event_loop
from json import dumps, loads
from typing import Dict, Union, Any

from websockets import connect

from pyscord._config import GatewayConfig


# TODO: Implement logging


class GatewayDispatch:
    """
    Represents a websocket message.
    """

    def __init__(self, op: int, data: Dict[str, Any], seq: int, name: str):
        """
        Instantiate a new GatewayDispatch object.

        :param op: The discord opcode which represents what the message
                    means.
        :param data: The event data that has been sent/received.
        :param seq: The sequence number of a message, which can be used
                    for resuming sessions and heartbeats.
        :param name: The event name for the payload.
        """
        self.op: int = op
        self.data: Dict = data
        self.seq: int = seq
        self.event_name: str = name

    def __str__(self) -> str:
        """
        :return The string representation of the GatewayDispatch object.
        This object can be used to send a websocket message to the gateway.
        """
        return dumps(
            dict(op=self.op, d=self.data, s=self.seq, t=self.event_name))

    @classmethod
    def from_string(cls, payload: str) -> GatewayDispatch:
        """
        Parses a given payload from a string format and returns a
        GatewayDispatch.

        :param payload: The payload to parse.
        :return: A proper GatewayDispatch object.
        """
        payload: Dict[str, Union[int, str, Dict[str, Any]]] = loads(payload)
        return cls(
            payload.get("op"),
            payload.get("d"),
            payload.get("s"),
            payload.get("t")
        )


class Dispatcher:
    """
    The Dispatcher handles all interactions with the discord websocket
    API. This also contains the main event loop, and handles the heartbeat.

    Running the dispatcher will create a connection with the
    Discord WebSocket API on behalf of the provided token. This token
    must be a bot token. (Which can be found on
    `/developers/applications/<bot_id>/bot`)
    """

    # TODO: Add intents argument
    # TODO: Add handlers argument
    def __init__(self, token: str):
        # TODO: Write docs for __init__.
        self.__token = token
        self.__keep_alive = True

    # TODO: Implement socket typehint
    async def handler_manager(self, socket, payload: GatewayDispatch):
        """
        This manages all handles for given OP codes.
        This method gets invoked for every message that is received from
        Discord.

        :param socket: The current socket, which can be used to interact
                with the Discord API.
        :param payload: The received payload from Discord.
        """
        # TODO: Implement heartbeat
        # TODO: Implement given handlers.
        # TODO: Implement logging
        pass

    async def __main(self):
        """
        The main event loop. This handles all interactions with the
        websocket API.
        """
        # TODO: Implement logging
        async with connect(GatewayConfig.uri()) as socket:
            while self.__keep_alive:
                await self.handler_manager(
                    socket,
                    GatewayDispatch.from_string(await socket.recv()))

    def run(self):
        """
        Instantiate the dispatcher, this will create a connection to the
        Discord websocket API on behalf of the client who's token has
        been passed.
        """
        # TODO: Implement logging
        loop = get_event_loop()
        loop.run_until_complete(self.__main())
        loop.close()

    def close(self):
        """
        Stop the dispatcher from listening and responding to gateway
        events. This should let the client close on itself.
        """
        # TODO: Implement logging
        self.__keep_alive = False
