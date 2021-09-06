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

from json import dumps, loads
from typing import Optional, Union, Dict, Any


class GatewayDispatch:
    """Represents a websocket message."""

    def __init__(
            self,
            op: int,
            data: Optional[Union[int, Dict[str, Any]]],
            seq: Optional[int] = None,
            name: Optional[str] = None
    ):
        """
        Instantiate a new GatewayDispatch object.

        :param op:
            The discord opcode which represents what the message means.

        :param data:
            The event data that has been sent/received.

        :param seq:
            The sequence number of a message, which can be used
            for resuming sessions and heartbeats.

        :param name:
            The event name for the payload.
        """
        self.op: int = op
        self.data: Optional[Union[int, Dict[str, Any]]] = data
        self.seq: Optional[int] = seq
        self.event_name: Optional[str] = name

    def __str__(self) -> str:
        """
        :return
            The string representation of the GatewayDispatch object.

        This can be used to send a websocket message to the gateway.
        """
        return dumps(
            dict(
                op=self.op,
                d=self.data,
                s=self.seq,
                t=self.event_name
            )
        )

    @classmethod
    def from_string(cls, payload: str) -> GatewayDispatch:
        """
        Parses a given payload from a string format
            and returns a GatewayDispatch.

        :param payload:
            The payload to parse.

        :return:
            A proper GatewayDispatch object.
        """
        payload: Dict[str, Union[int, str, Dict[str, Any]]] = loads(payload)
        return cls(
            payload.get("op"),
            payload.get("d"),
            payload.get("s"),
            payload.get("t")
        )
