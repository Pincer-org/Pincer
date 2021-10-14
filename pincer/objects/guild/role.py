# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils import APINullable, Snowflake


@dataclass
class RoleTags(APIObject):
    """
    Special tags/flags which have been defined for a role.

    :bot_id:
        The id of the bot this role belongs to.
        (the role got created by adding the bot with this id)

    :integration_id:
        The id of the integration this role belongs to.
        (the role got created by adding an integration with this id)

    :premium_subscriber:
        Whether this is the guild's premium subscriber role or not.
    """
    bot_id: APINullable[Snowflake] = MISSING
    integration_id: APINullable[Snowflake] = MISSING
    premium_subscriber: APINullable[bool] = MISSING


@dataclass
class Role(APIObject):
    """
    Represents a Discord guild/server role.

    :param color:
        integer representation of hexadecimal color code

    :param hoist:
        if this role is pinned in the user listing

    :param id:
        role id

    :param managed:
        whether this role is managed by an integration

    :param mentionable:
        whether this role is mentionable

    :param name:
        role name

    :param permissions:
        permission bit set

    :param position:
        position of this role

    :param tags:
        the tags this role has

    :param mention:
        structures a string to mention the role
    """

    color: int
    hoist: bool
    id: Snowflake
    managed: bool
    mentionable: bool
    name: str
    permissions: str
    position: int

    icon: APINullable[str] = MISSING
    unicode_emoji: APINullable[str] = MISSING
    tags: APINullable[RoleTags] = MISSING

    @property
    def mention(self):
        return f"<@&{self.id}>"

    # TODO: Implement Caching
    @classmethod
    async def from_id(cls, client, guild_id: int, role_id: int) -> Role:
        roles: list = await client.http.get(f"/guilds/{guild_id}/roles")

        for role in roles:
            if int(role['id']) == role_id:
                return cls.from_dict(role)
