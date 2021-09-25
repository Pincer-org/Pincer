# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from pincer.core.http import HTTPClient

from .user import User
from ..utils import APIObject, APINullable, MISSING, Snowflake, Timestamp, \
    convert

if TYPE_CHECKING:
    from .. import Client


@dataclass
class GuildMember(APIObject):
    """
    Represents a member which resides in a guild/server.

    :param _client:
        reference to the Client

    :param _http:
        reference to the HTTPClient

    :param deaf:
        whether the user is deafened in voice channels

    :param joined_at:
        when the user joined the guild

    :param mute:
        whether the user is muted in voice channels

    :param roles:
        array of role object ids

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

    _client: Client
    _http: HTTPClient

    deaf: bool
    joined_at: Timestamp
    mute: bool
    roles: List[Snowflake]

    hoisted_role: APINullable[Snowflake] = MISSING
    nick: APINullable[Optional[str]] = MISSING
    pending: APINullable[bool] = MISSING
    is_pending: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_since: APINullable[Optional[Timestamp]] = MISSING
    user: APINullable[User] = MISSING
    avatar: APINullable[str] = MISSING

    def __post_init__(self):
        self.roles = convert(self.roles, Snowflake.from_string)
        self.user = convert(self.user, User.from_dict, User, self._client)
        self.premium_since = convert(
            self.premium_since, Timestamp.parse, Timestamp
        )

    @classmethod
    async def from_id(
            cls,
            client: Client,
            guild_id: int,
            _id: int
    ) -> GuildMember:
        data = await client.http.get(f"guilds/{guild_id}/members/{_id}")
        return cls.from_dict(data | {"_client": client, "_http": client.http})
