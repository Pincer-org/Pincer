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
from typing import Any, List, Optional

from .presence import PresenceUpdateEvent
from ..objects.guild_member import GuildMember
from ..objects.emoji import Emoji
from ..objects.role import Role
from ..objects.sticker import Sticker
from ..objects.user import User
from ..utils.api_object import APIObject
from ..utils.snowflake import Snowflake
from ..utils.timestamp import Timestamp
from ..utils.types import MISSING, APINullable

@dataclass
class GuildBanAddEvent(APIObject):
    """
    Sent when a user is banned from a guild.

    :param guild_id:
        id of the guild

    :param user:
        the banned user
    """
    guild_id: Snowflake
    user: User

@dataclass
class GuildBanRemoveEvent(APIObject):
    """
    Sent when a user is unbanned from a guild.

    :param guild_id:
        id of the guild

    :param user:
        the unbanned user
    """
    guild_id: Snowflake
    user: User

@dataclass
class GuildEmojisUpdateEvent(APIObject):
    """
    Sent when a guild's emojis have been updated.

    :param guild_id:
        id of the guild

    :param emojis:
        array of emojis
    """
    guild_id: Snowflake
    emojis: List[Emoji]

@dataclass
class GuildStickersUpdateEvent(APIObject):
    """
    Sent when a guild's stickers have been updated.

    :param guild_id:
        id of the guild

    :param stickers:
        array of stickers
    """
    guild_id: Snowflake
    stickers: List[Sticker]

@dataclass
class GuildIntegrationsUpdateEvent(APIObject):
    """
    Sent when a guild integration is updated.

    :param guild_id:
        id of the guild whose integrations were updated
    """
    guild_id: Snowflake

@dataclass
class GuildMemberRemoveEvent(APIObject):
    """
    Sent when a user is removed from a guild (leave/kick/ban).

    :param guild_id:
        the id of the guild

    :param user:
        the user who was removed
    """
    guild_id: Snowflake
    user: User

@dataclass
class GuildMemberUpdateEvent(APIObject):
    """
    Sent when a guild member is updated.
    This will also fire when the user object
    of a guild member changes.

    :param guild_id:
        the id of the guild

    :param roles:
        user role ids

    :param user:
        the user

    :param nick:
        nickname of the user in the guild

    :param joined_at:
        when the user joined the guild

    :param premium_since:
        when the user started boosting the guild

    :param deaf:
        whether the user is deafened in voice channels

    :param mute:
        whether the user is muted in voice channels

    :param pending:
        whether the user has not yet passed the guild's
        Membership Screening requirements
    """
    guild_id: Snowflake
    roles: List[Snowflake]
    user: User
    nick: APINullable[Optional[str]] = MISSING
    joined_at: Optional[Timestamp] = None
    premium_since: APINullable[Optional[Timestamp]] = MISSING
    deaf: APINullable[bool] = MISSING
    mute: APINullable[bool] = MISSING
    pending: APINullable[bool] = MISSING

@dataclass
class GuildMembersChunkEvent(APIObject):
    """
    Sent in response to Guild Request Members.
    You can use the `chunk_index` and `chunk_count`
    to calculate how many chunks are left for your request.

    :param guild_id:
        the id of the guild

    :param members:
        set of guild members

    :param chunk_index:
        the chunk index in the expected chunks for this response
        (0 <= chunk_index < chunk_count)

    :param chunk_count:
        the total number of expected chunks for this response

    :param not_found:
        if passing an invalid id to `REQUEST_GUILD_MEMBERS`,
        it will be returned here

    :param presences:
        if pasing true to `REQUEST_GUILD_MEMBERS`, presences
        of the returned members will be here

    :param nonce:"
        the nonce used in the Guild Members Request
    """
    guild_id: Snowflake
    members: List[GuildMember]
    chunk_index: int
    chunk_count: int

    not_found: APINullable[List[Any]] = MISSING
    presences: APINullable[PresenceUpdateEvent] = MISSING
    nonce: APINullable[str] = MISSING

@dataclass
class GuildRoleCreateEvent(APIObject):
    """
    Sent when a guild role is created.

    :param guild_id:
        the id of the guild

    :param role:
        the role created
    """
    guild_id: Snowflake
    role: Role

@dataclass
class GuildRoleUpdateEvent(APIObject):
    """
    Sent when a guild role is updated.

    :param guild_id:
        the id of the guild

    :param role:
        the role updated
    """
    guild_id: Snowflake
    role: Role

@dataclass
class GuildRoleDeleteEvent(APIObject):
    """
    Sent when a guild role is deleted.
    
    :param guild_id:
        id of the guild

    :param role_id:
        id of the role
    """
    guild_id: Snowflake
    role_id: Snowflake