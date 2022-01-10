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


@dataclass(repr=False)
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

    joined_at: APINullable[Timestamp] = MISSING
    roles: APINullable[List[Snowflake]] = MISSING
    deaf: bool = MISSING
    mute: bool = MISSING

    hoisted_role: APINullable[Snowflake] = MISSING


@dataclass(repr=False)
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


@dataclass(repr=False)
class GuildMember(BaseMember, User):
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
    avatar: APINullable[:class:`str`]
        The user's avatar.
    communication_disabled_until: APINullable[Optional[:class:`~pincer.utils.timestamp.Timestamp`]]
        The timestamp at which the user is no longer timed out.

        .. note::

            This may be in the past if the user has been timed out recently.

    """  # noqa: E501

    nick: APINullable[Optional[str]] = MISSING
    pending: APINullable[bool] = MISSING
    is_pending: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_since: APINullable[Optional[Timestamp]] = MISSING
    user: APINullable[User] = MISSING
    avatar: APINullable[str] = MISSING
    communication_disabled_until: APINullable[Optional[Timestamp]] = MISSING

    def __post_init__(self):
        super().__post_init__()

        if self.user is not MISSING:
            self.set_user_data(self.user)

    def set_user_data(self, user: User):
        """
        Used to set the user parameters of a GuildMember instance

        user: APINullable[:class:`~pincer.objects.user.user.User`]
            A user class to copy the fields from
        """

        # Inspired from this thread
        # https://stackoverflow.com/questions/57962873/easiest-way-to-copy-all-fields-from-one-dataclass-instance-to-another

        for key, value in user.__dict__.items():
            setattr(self, key, value)

        self.user = MISSING

    @classmethod
    async def from_id(
        cls, client: Client, guild_id: int, user_id: int
    ) -> GuildMember:
        data = await client.http.get(f"guilds/{guild_id}/members/{user_id}")
        return cls.from_dict(data)
