# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..user.user import User
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.timestamp import Timestamp
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List, Optional

    from ...client import Client
    from ...utils.types import APINullable


@dataclass
class BaseMember(APIObject):
    """Represents the base of a guild member.

    Attributes
    ----------
    deaf: :class:`bool`
        Whether the user is deafened in voice channels
    joined_at: :class:`~pincer.utils.timestamp.Timestamp`
        Then the user joined the guild
    mute: :class:`bool`
        Whether the user is muted in voice channels
    roles: List[:class:`~pincer.utils.snowflake.Snowflake`]
        Array of role object ids
    hoisted_role: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The user's top role in the guild.
    """
    deaf: bool
    joined_at: Timestamp
    mute: bool
    roles: List[Snowflake]

    hoisted_role: APINullable[Snowflake] = MISSING


@dataclass
class PartialGuildMember(APIObject):
    """Represents a partial guild member.
    This is a reference to a member from a guild which does not contain
    all information.

    This gets used in form example message mentions.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The user's id
    username: :class:`str`
        The user's username, not unique across the platform
    discriminator: :class:`str`
        The user's 4-digit discord-tag
    avatar: :class:`str`
        The user's avatar hash
    public_flags: :class:`int`
        The flags on a user's account
    member: :class:`~pincer.objects.guild.member.BaseMember`
        The user their (partial) guild information.
    """
    id: Snowflake
    username: str
    discriminator: str
    avatar: str
    public_flags: int
    member: Optional[BaseMember]


@dataclass
class GuildMember(BaseMember, APIObject):
    """Represents a member which resides in a guild/server.

    Attributes
    ----------
    nick: APINullable[Optional[:class:`str`]]
        This users guild nickname
    pending: APINullable[:class:`bool`]
        Whether the user has not yet passed the guild's Membership
        Screening requirements
    is_pending: APINullable[:class:`bool`]
        Deprecated version of pending.
    permissions: APINullable[:class:`str`]
        Total permissions of the member in the channel,
        including overwrites, returned when in the interaction object
    premium_since: APINullable[Optional[:class:`~pincer.utils.timestamp.Timestamp`]]
        When the user started boosting the guild
    user: APINullable[:class:`~pincer.objects.user.user.User`]
        The user this guild member represents
    Avatar: APINullable[:class:`str`]
        The user's avatar.
    """  # noqa: E501

    nick: APINullable[Optional[str]] = MISSING
    pending: APINullable[bool] = MISSING
    is_pending: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_since: APINullable[Optional[Timestamp]] = MISSING
    user: APINullable[User] = MISSING
    avatar: APINullable[str] = MISSING

    @classmethod
    async def from_id(
            cls,
            client: Client,
            guild_id: int,
            _id: int
    ) -> GuildMember:
        data = await client.http.get(f"guilds/{guild_id}/members/{_id}")
        return cls.from_dict({**data, "_client": client, "_http": client.http})
