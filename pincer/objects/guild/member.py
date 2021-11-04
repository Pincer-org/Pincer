# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from ..user import User
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.timestamp import Timestamp
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ... import Client
    from ...utils.types import APINullable


@dataclass
class BaseMember(APIObject):
    """
    Represents the base of a guild member.

    :param deaf:
        whether the user is deafened in voice channels

    :param joined_at:
        when the user joined the guild

    :param mute:
        whether the user is muted in voice channels

    :param roles:
        array of role object ids

    :param hoisted_role:
        The user their top guild role!
    """
    deaf: bool
    joined_at: Timestamp
    mute: bool
    roles: List[Snowflake]

    hoisted_role: APINullable[Snowflake] = MISSING


@dataclass
class PartialGuildMember(APIObject):
    """
    Represents a partial guild member.
    This is a reference to a member from a guild which does not contain
    all information.

    This gets used in form example message mentions.

    :param id:
        the user's id

    :param username:
        the user's username, not unique across the platform

    :param discriminator:
        the user's 4-digit discord-tag

    :param avatar:
        the user's avatar hash

    :param public_flags:
        the flags on a user's account

    :param member:
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
    """
    Represents a member which resides in a guild/server.

    :param _client:
        reference to the Client

    :param _http:
        reference to the HTTPClient

    :param nick:
        this users guild nickname

    :param pending:
        whether the user has not yet passed the guild's Membership
        Screening requirements

    :param is_pending:
        Deprecated version of pending.

    :param permissions:
        total permissions of the member in the channel,
        including overwrites, returned when in the interaction object

    :param premium_since:
        when the user started boosting the guild

    :param user:
        the user this guild member represents
    """

    # _client: Client
    # _http: HTTPClient

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
