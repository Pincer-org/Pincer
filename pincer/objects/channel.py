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
from enum import Enum
from typing import Optional, Union, List

from websockets.typing import Data

from pincer._config import GatewayConfig
from pincer.utils.api_object import APIObject


class ChannelType(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6

    if GatewayConfig.version >= 9:
        GUILD_NEWS_THREAD = 10
        GUILD_PUBLIC_THREAD = 11
        GUILD_PRIVATE_THREAD = 12

    GUILD_STAGE_VOICE = 13


@dataclass
class Channel(APIObject):
    id: int
    type: ChannelType
    guild_id: Optional[int] = None
    position: Optional[int] = None
    permission_overwrites: Optional[List[...]] = None
    name: Optional[str] = None
    topic: Optional[str] = None
    nsfw: Optional[bool] = None
    last_message_id: Optional[int] = None
    bitrate: Optional[int] = None
    user_limit: Optional[int] = None
    rate_limit_per_user: Optional[int] = None
    recipients: Optional[List[...]] = None
    icon: Optional[str] = None
    owner_id: Optional[int] = None
    application_id: Optional[int] = None
    parent_id: Optional[int] = None
    last_pin_timestamp: Optional[str] = None
    rtc_region: Optional[str] = None
    video_quality_mode: Optional[int] = None
    message_count: Optional[int] = None
    member_count: Optional[int] = None
    thread_metadata: Optional[...] = None
    member: Optional[...] = None
    default_auto_archive_duration: Optional[int] = None
    permissions: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Data[str, Union[str, bool, int]]) -> Channel:
        # TODO: Write documentation
        return cls(**data)

    def __str__(self):
        """return the discord tag when object gets used as a string."""
        return self.name or str(self.id)
