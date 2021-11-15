# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..guild.guild import Guild
from ..guild.member import GuildMember
from ..user import User
from ...utils.api_object import APIObject
from ...utils.conversion import construct_client_dict
from ...utils.types import MISSING, APINullable

if TYPE_CHECKING:
    from typing import Any, List, Optional

    from ..guild.role import Role
    from ..message.emoji import Emoji
    from ..message.sticker import Sticker
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp
    from .presence import PresenceUpdateEvent


@dataclass
class GuildBanAddEvent(APIObject):
    """Sent when a user is banned from a guild.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild
    user: :class:`~pincer.objects.user.user.User`
        The banned user
    """

    guild_id: Snowflake
    user: User


@dataclass
class GuildBanRemoveEvent(APIObject):
    """Sent when a user is unbanned from a guild.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild
    user: :class:`~pincer.objects.user.user.User`
        The unbanned user
    """

    guild_id: Snowflake
    user: User


@dataclass
class GuildEmojisUpdateEvent(APIObject):
    """Sent when a guild's emojis have been updated.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild
    emojis: List[:class:`~pincer.objects.message.emoji.Emoji`]
        Array of emojis
    """

    guild_id: Snowflake
    emojis: List[Emoji]


@dataclass
class GuildStickersUpdateEvent(APIObject):
    """Sent when a guild's stickers have been updated.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild
    stickers: List[:class:`~pincer.objects.message.sticker.Sticker`]
        Array of stickers
    """

    guild_id: Snowflake
    stickers: List[Sticker]


@dataclass
class GuildIntegrationsUpdateEvent(APIObject):
    """Sent when a guild integration is updated.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild whose integrations were updated
    """

    guild_id: Snowflake


@dataclass
class GuildMemberAddEvent(GuildMember):
    """
    Sent when a user joins a guild.

    Attributes
    ----------
    guild_id: :class:`Snowflake`
        ID of the guild that the user joined.
    """

    # NOTE: This isn't a default value. I set it to this because you can't
    # have fields without default values after regular fields. Apparently that
    # carries over when you inherit from a dataclass.
    guild_id: Snowflake = 0


@dataclass
class GuildMemberRemoveEvent(APIObject):
    """Sent when a user is removed from a guild (leave/kick/ban).

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        the id of the guild
    user: :class:`~pincer.objects.user.user.User`
        the user who was removed
    """

    guild_id: Snowflake
    user: User

    def __post_init__(self):
        self.user = User.from_dict(
            construct_client_dict(self._client, self.user)
        )


@dataclass
class GuildMemberUpdateEvent(APIObject):
    """Sent when a guild member is updated.
    This will also fire when the user object
    of a guild member changes.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        the id of the guild
    roles: List[:class:`~pincer.utils.snowflake.Snowflake`]
        user role ids
    user: :class:`~pincer.objects.user.user.User`
        the user
    nick: APINullable[Optional[:class:`str`]]
        nickname of the user in the guild
    joined_at: Optional[:class:`~pincer.utils.timestamp.Timestamp`]
        when the user joined the guild
    premium_since: APINullable[Optional[:class:`~pincer.utils.timestamp.Timestamp`]]
        when the user started boosting the guild
    deaf: APINullable[:class:`bool`]
        whether the user is deafened in voice channels
    mute: APINullable[:class:`bool`]
        whether the user is muted in voice channels
    pending: APINullable[:class:`bool`]
        whether the user has not yet passed the guild's
        Membership Screening requirements
    """
    # noqa: E501

    guild_id: Snowflake
    roles: List[Snowflake]
    user: User
    nick: APINullable[Optional[str]] = MISSING
    joined_at: Optional[Timestamp] = None
    premium_since: APINullable[Optional[Timestamp]] = MISSING
    deaf: APINullable[bool] = MISSING
    mute: APINullable[bool] = MISSING
    pending: APINullable[bool] = MISSING

    def __post_init__(self):
        self.user = User.from_dict(
            construct_client_dict(self._client, self.user)
        )


@dataclass
class GuildMembersChunkEvent(APIObject):
    """Sent in response to Guild Request Members.
    You can use the ``chunk_index`` and ``chunk_count``
    to calculate how many chunks are left for your request.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the guild
    members: List[:class:`~pincer.objects.guild.member.GuildMember`]
        Set of guild members
    chunk_index: :class:`int`
        The chunk index in the expected chunks for this response
        (0 <= chunk_index < chunk_count)
    chunk_count: :class:`int`
        The total number of expected chunks for this response
    not_found: APINullable[List[Any]]
        If passing an invalid id to ``REQUEST_GUILD_MEMBERS``,
        it will be returned here
    presences: APINullable[:class:`~pincer.objects.events.presence.PresenceUpdateEvent`]
        If passing true to ``REQUEST_GUILD_MEMBERS``, presences
        of the returned members will be here
    nonce: APINullable[:class:`str`]
        The nonce used in the Guild Members Request
    """
    # noqa: E501
    guild_id: Snowflake
    members: List[GuildMember]
    chunk_index: int
    chunk_count: int

    not_found: APINullable[List[Any]] = MISSING
    presences: APINullable[PresenceUpdateEvent] = MISSING
    nonce: APINullable[str] = MISSING

    def __post_init__(self):
        self.members = [
            GuildMember.from_dict(construct_client_dict(self._client, member))
            for member in self.members
        ]


@dataclass
class GuildRoleCreateEvent(APIObject):
    """Sent when a guild role is created.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the guild
    role: :class:`~pincer.objects.guild.role.Role`
        The role created
    """

    guild_id: Snowflake
    role: Role


@dataclass
class GuildRoleUpdateEvent(APIObject):
    """Sent when a guild role is updated.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the guild
    role: :class:`~pincer.objects.guild.role.Role`
        The role updated
    """

    guild_id: Snowflake
    role: Role


@dataclass
class GuildRoleDeleteEvent(APIObject):
    """Sent when a guild role is deleted.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild
    role_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the role
    """

    guild_id: Snowflake
    role_id: Snowflake


@dataclass
class GuildStatusEvent(APIObject):
    """
    Sent when a subscribed server's state changes

    Attributes
    ----------
    guild : :class:`Guild`
        guild with requested id

    online : :class:`int`
        number of online users in guild (deprecated; always 0)
    """

    guild: Guild
    online: int = 0
