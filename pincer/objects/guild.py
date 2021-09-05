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
import logging
from typing import Optional, List

from pincer.exceptions import PincerError
from pincer.objects.channel import Channel
from pincer.objects.emoji import Emoji
from pincer.objects.member import Member
from pincer.objects.role import Role
from pincer.objects.stage import StageInstance
from pincer.objects.sticker import Sticker
from pincer.objects.welcome_screen import WelcomeScreen
from pincer.utils.api_object import APIObject
from pincer.utils.constants import OptionallyProvided, MISSING
from pincer.utils.snowflake import Snowflake
from pincer.utils.timestamp import Timestamp


class UnavailableGuildError(PincerError):
    pass


@dataclass
class Guild(APIObject):
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    application_id: Optional[int]
    banner: Optional[str]
    default_message_notifications: int
    description: Optional[str]
    discovery_splash: Optional[str]
    emojis: List[Emoji]
    explicit_content_filter: int
    features: List[...]
    id: Snowflake
    icon: Optional[str]
    mfa_level: int
    name: str
    nsfw_level: int
    owner_id: Snowflake
    preferred_locale: str
    premium_tier: int
    public_updates_channel_id: Optional[Snowflake]
    roles: List[Role]
    rules_channel_id: Optional[int]
    splash: Optional[str]
    system_channel_flags: int
    system_channel_id: Optional[int]
    vanity_url_code: Optional[str]
    verification_level: int

    approximate_member_count: OptionallyProvided[int] = MISSING
    approximate_presence_count: OptionallyProvided[int] = MISSING
    channels: OptionallyProvided[List[Channel]] = MISSING
    icon_hash: OptionallyProvided[Optional[str]] = MISSING
    joined_at: OptionallyProvided[Timestamp] = MISSING
    large: OptionallyProvided[bool] = MISSING
    max_members: OptionallyProvided[int] = MISSING
    max_presences: OptionallyProvided[Optional[int]] = MISSING
    max_video_channel_users: OptionallyProvided[int] = MISSING
    members: OptionallyProvided[List[Member]] = MISSING
    member_count: OptionallyProvided[bool] = MISSING
    owner: OptionallyProvided[bool] = MISSING
    permissions: OptionallyProvided[str] = MISSING
    premium_subscription_count: OptionallyProvided[int] = MISSING
    presences: OptionallyProvided[List[...]] = MISSING
    stage_instances: OptionallyProvided[List[StageInstance]] = MISSING
    stickers: OptionallyProvided[List[Sticker]] = MISSING
    region: OptionallyProvided[Optional[str]] = MISSING
    threads: OptionallyProvided[List[Channel]] = MISSING
    # Guilds are considered available unless otherwise specified
    unavailable: bool = False
    voice_states: OptionallyProvided[bool] = MISSING
    widget_enabled: OptionallyProvided[bool] = MISSING
    widget_channel_id: OptionallyProvided[Optional[Snowflake]] = MISSING
    welcome_screen: OptionallyProvided[WelcomeScreen] = MISSING

    @classmethod
    def from_dict(cls, data, *args, **kwargs) -> Guild:
        if data.get("unavailable", False):
            raise UnavailableGuildError(
                f"Guild \"{data['id']}\" is unavailable due"
                " to a discord outage."
            )
        return super().from_dict(data, *args, **kwargs)
