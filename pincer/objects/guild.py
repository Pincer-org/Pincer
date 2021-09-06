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

from pincer.exceptions import UnavailableGuildError
from pincer.objects.channel import Channel
from pincer.objects.emoji import Emoji
from pincer.objects.member import Member
from pincer.objects.role import Role
from pincer.objects.stage import StageInstance
from pincer.objects.sticker import Sticker
from pincer.objects.welcome_screen import WelcomeScreen
from pincer.utils.api_object import APIObject
from pincer.utils.constants import APINullable, MISSING
from pincer.utils.snowflake import Snowflake
from pincer.utils.timestamp import Timestamp


@dataclass
class Guild(APIObject):
    """
    :param id:
        guild id
    :param name:
        guild name (2-100 characters, excluding trailing and leading
        whitespace)
    :param icon:
        icon hash
    :param icon_hash:
        icon hash, returned when in the template object
    :param splash:
        splash hash
    :param discovery_splash:
        discovery splash hash; only present for guilds with the DISCOVERABLE
        feature
    :param owner:
        true if the user is the owner of the guild
    :param owner_id:
        id of owner
    :param permissions:
        total permissions for the user in the guild (excludes overwrites)
    :param region:
        voice region id for the guild (deprecated)
    :param afk_channel_id:
        id of afk channel
    :param afk_timeout:
        afk timeout in seconds
    :param widget_enabled:
        true if the server widget is enabled
    :param widget_channel_id:
        the channel id that the widget will generate an invite to, or null if
        set to no invite
    :param verification_level:
        verification level required for the guild
    :param default_message_notifications:
        default message notifications level
    :param explicit_content_filter:
        explicit content filter level
    :param roles:
        roles in the guild
    :param emojis:
        custom guild emojis
    :param features:
        enabled guild features
    :param mfa_level:
        required MFA level for the guild
    :param application_id:
        application id of the guild creator if it is bot-created
    :param system_channel_id:
        the id of the channel where guild notices such as welcome messages and
        boost events are posted
    :param system_channel_flags:
        system channel flags
    :param rules_channel_id:
        the id of the channel where Community guilds can display rules and/or
        guidelines
    :param joined_at:
        when this guild was joined at
    :param large:
        true if this is considered a large guild
    :param unavailable:
        true if this guild is unavailable due to an outage
    :param member_count:
        total number of members in this guild
    :param voice_states:
        states of members currently in voice channels; lacks the guild_id key
    :param members:
        users in the guild
    :param channels:
        channels in the guild
    :param threads:
        all active threads in the guild that current user has permission to
        view
    :param presences:
        presences of the members in the guild, will only include non-offline
        members if the size is greater than large threshold
    :param max_presences:
        the maximum number of presences for the guild (null is always
        returned, apart from the largest of guilds)
    :param max_members:
        the maximum number of members for the guild
    :param vanity_url_code:
        the vanity url code for the guild
    :param description:
        the description of a Community guild
    :param banner:
        banner hash
    :param premium_tier:
        premium tier (Server Boost level)
    :param premium_subscription_count:
        the number of boosts this guild currently has
    :param preferred_locale:
        the preferred locale of a Community guild; used in server discovery
        and notices from Discord; defaults to en-US
    :param public_updates_channel_id:
        the id of the channel where admins and moderators of Community guilds
        receive notices from Discord
    :param max_video_channel_users:
        the maximum amount of users in a video channel
    :param approximate_member_count:
        approximate number of members in this guild, returned from the
        GET /guilds/<id> endpoint when with_counts is true
    :param approximate_presence_count:
        approximate number of non-offline members in this guild, returned from
        the GET /guilds/<id> endpoint when with_counts is true
    :param welcome_screen:
        the welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    :param nsfw_level:
        guild NSFW level
    :param stage_instances:
        Stage instances in the guild
    :param stickers:
        custom guild stickers
    """

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

    approximate_member_count: APINullable[int] = MISSING
    approximate_presence_count: APINullable[int] = MISSING
    channels: APINullable[List[Channel]] = MISSING
    icon_hash: APINullable[Optional[str]] = MISSING
    joined_at: APINullable[Timestamp] = MISSING
    large: APINullable[bool] = MISSING
    max_members: APINullable[int] = MISSING
    max_presences: APINullable[Optional[int]] = MISSING
    max_video_channel_users: APINullable[int] = MISSING
    members: APINullable[List[Member]] = MISSING
    member_count: APINullable[bool] = MISSING
    owner: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_subscription_count: APINullable[int] = MISSING
    presences: APINullable[List[...]] = MISSING
    stage_instances: APINullable[List[StageInstance]] = MISSING
    stickers: APINullable[List[Sticker]] = MISSING
    region: APINullable[Optional[str]] = MISSING
    threads: APINullable[List[Channel]] = MISSING
    # Guilds are considered available unless otherwise specified
    unavailable: APINullable[bool] = MISSING
    voice_states: APINullable[bool] = MISSING
    widget_enabled: APINullable[bool] = MISSING
    widget_channel_id: APINullable[Optional[Snowflake]] = MISSING
    welcome_screen: APINullable[WelcomeScreen] = MISSING

    @classmethod
    def from_dict(cls, data) -> Guild:
        if data.get("unavailable", False):
            raise UnavailableGuildError(
                f"Guild \"{data['id']}\" is unavailable due"
                " to a discord outage."
            )
        return super().from_dict(data)
