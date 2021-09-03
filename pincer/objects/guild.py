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
from typing import Optional, List


from pincer.objects.emoji import Emoji
from pincer.objects.role import Role
from pincer.objects.member import Member
from pincer.objects.channel import Channel
from pincer.objects.sticker import Sticker
from pincer.utils.api_object import APIObject

@dataclass
class Guild(APIObject):
    id: int
    name: str

    owner_id: int
    afk_timeout: int

    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    system_channel_flags: int

    roles: List[Role]
    emojis: List[Emoji]
    features: List[...]
    mfa_level: int
    premium_tier: int
    preferred_locale: str
    nsfw_level: int

    application_id: Optional[int] = None
    system_channel_id: Optional[int] = None
    rules_channel_id: Optional[int] = None

    icon: Optional[str] = None
    icon_hash: Optional[str] = None
    splash: Optional[str] = None
    discovery_splash: Optional[str] = None
    owner: Optional[bool] = None
    permissions: Optional[str] = None
    region: Optional[str] = None
    afk_channel_id: Optional[int] = None
    widget_enabled: Optional[bool] = None
    widget_channel_id: Optional[bool] = None

    joined_at: Optional[str] = None
    large: Optional[bool] = None
    unavailable: Optional[bool] = None
    member_count: Optional[bool] = None
    voice_states: Optional[bool] = None
    members: Optional[List[Member]] = None
    channels: Optional[List[Channel]] = None
    threads: Optional[List[...]] = None
    presences: Optional[List[...]] = None
    max_presences: Optional[int] = None
    max_members: Optional[int] = None
    vanity_url_code: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None

    premium_subscription_count: Optional[int] = None
    public_updates_channel_id: Optional[int] = None
    max_video_channel_users: Optional[int] = None
    approximate_member_count: Optional[int] = None
    approximate_presence_count: Optional[int] = None
    welcome_screen: Optional[...] = None
    stage_instances: Optional[List[...]] = None
    stickers: Optional[List[Sticker]] = None
