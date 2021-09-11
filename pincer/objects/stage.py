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

from dataclasses import dataclass
from enum import IntEnum

from ..utils import APIObject, Snowflake


class PrivacyLevel(IntEnum):
    """
    Represents the level of publicity of a stage.
    """
    PUBLIC = 1
    GUILD_ONLY = 2


@dataclass
class StageInstance(APIObject):
    """
    Represents a Stage Instance object


    :param id:
        id of this Stage instance

    :param guild_id:
        guild id of the associated Stage channel

    :param channel_id:
        id of the associated Stage channel

    :param topic:
        topic of the Stage instance (1-120 characters)

    :param privacy_level:
        privacy level of the Stage instance

    :param discoverable:
        is Stage Discovery enabled
    """
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable: bool

    @property
    def discoverable_disabled(self) -> bool:
        return not self.discoverable
