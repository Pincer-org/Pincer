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
from typing import Optional, List

from pincer._config import GatewayConfig
from pincer.objects.member import Member
from pincer.objects.user import User
from pincer.utils.api_object import APIObject
from pincer.utils.constants import OptionallyProvided, MISSING


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

    application_id: OptionallyProvided[int] = MISSING
    bitrate: OptionallyProvided[int] = MISSING
    default_auto_archive_duration: OptionallyProvided[int] = MISSING
    guild_id: OptionallyProvided[int] = MISSING
    icon: OptionallyProvided[Optional[str]] = MISSING
    last_message_id: OptionallyProvided[Optional[int]] = MISSING
    last_pin_timestamp: OptionallyProvided[Optional[str]] = MISSING
    member: OptionallyProvided[Member] = MISSING
    member_count: OptionallyProvided[int] = MISSING
    message_count: OptionallyProvided[int] = MISSING
    name: OptionallyProvided[str] = MISSING
    nsfw: OptionallyProvided[bool] = MISSING
    owner_id: OptionallyProvided[int] = MISSING
    parent_id: OptionallyProvided[Optional[int]] = MISSING
    permissions: OptionallyProvided[str] = MISSING
    permission_overwrites: OptionallyProvided[List[...]] = MISSING
    position: OptionallyProvided[int] = MISSING
    rate_limit_per_user: OptionallyProvided[int] = MISSING
    recipients: OptionallyProvided[List[User]] = MISSING
    rtc_region: OptionallyProvided[Optional[str]] = MISSING
    thread_metadata: OptionallyProvided[...] = MISSING
    topic: OptionallyProvided[Optional[str]] = MISSING
    user_limit: OptionallyProvided[int] = MISSING
    video_quality_mode: OptionallyProvided[int] = MISSING

    def __str__(self):
        """return the discord tag when object gets used as a string."""
        return self.name or str(self.id)
