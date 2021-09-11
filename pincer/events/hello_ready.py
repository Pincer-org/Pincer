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

from dataclasses import dataclass
from typing import List, Tuple

from ..objects.application import Application
from ..objects.guild import Guild
from ..objects.user import User
from ..utils.api_object import APIObject
from ..utils.types import MISSING, APINullable

@dataclass
class HelloEvent(APIObject):
    """
    Sent on connection to the websocket.
    Defines the heartbeat interval that the client should heartbeat to.

    :param heartbeat_interval:
        the interval (in milliseconds) the client should hearbeat with
    """
    heartbeat_interval: int

@dataclass
class ReadyEvent(APIObject):
    """
    Dispatched when a client has completed the initial
    handshake with the gateway (for new sessions).

    :param v:
        gateway version

    :param user:
        information about the user including email

    :param guilds:
        the guilds the user is in

    :param session_id:
        used for resuming connections

    :param shard:
        the shard information associated
        with this session, if sent when identifying

    :param application:
        containts `id` and `flags`
    """
    v: int
    user: User
    guilds: List[Guild]
    session_id: str
    application: Application

    shard: APINullable[Tuple[int, int]] = MISSING