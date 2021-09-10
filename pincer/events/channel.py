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

from ..utils.api_object import APIObject
from ..utils.snowflake import Snowflake
from ..utils.timestamp import Timestamp
from ..utils.types import MISSING, APINullable

@dataclass
class ChannelPinsUpdateEvent(APIObject):
    """
    Sent when a message is pinned or unpinned in a text channel.
    This is not sent when a pinned message is deleted.

    :param guild_id:
        the id of the guild

    :param channel_id:
        the id of the channel

    :param last_pin_timestamp:
        the time at which the most recent pinned message was pinned
    """
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING
    last_pin_timestamp: APINullable[Timestamp] = MISSING