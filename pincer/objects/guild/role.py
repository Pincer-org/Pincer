# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


@dataclass
class RoleTags(APIObject):
    """Special tags/flags which have been defined for a role.

    Attributes
    ----------
    bot_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the bot this role belongs to.
        (the role got created by adding the bot with this id)
    integration_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the integration this role belongs to.
        (the role got created by adding an integration with this id)
    premium_subscriber: APINullable[:class:`bool`]
        Whether this is the guild's premium subscriber role or not.
    """
    bot_id: APINullable[Snowflake] = MISSING
    integration_id: APINullable[Snowflake] = MISSING
    premium_subscriber: APINullable[bool] = MISSING


@dataclass
class Role(APIObject):
    """
    Represents a Discord guild/server role.

    Attributes
    ----------
    color: :class:`int`
        Integer representation of hexadecimal color code
    hoist: :class:`bool`
        If this role is pinned in the user listing
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Role id
    managed: :class:`bool`
        Whether this role is managed by an integration
    mentionable: :class:`bool`
        Whether this role is mentionable
    name: :class:`str`
        Role name
    permissions:
        Permission bit set
    position: :class:`int`
        Position of this role
    icon: APINullable[:class:`str`]
        The role's icon
    unicode_emoji: APINullable[:class:`str`]
        The unicode emoji for this role
    tags: :class:`~pincer.objects.guild.role.RoleTags`
        The tags this role has
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
    def mention(self) -> str:
        """:class:`str`\\: Returns the mention string for this role."""
        return f"<@&{self.id}>"

    # TODO: Implement Caching @Arthurdw
    @classmethod
    async def from_id(cls, client, guild_id: int, role_id: int) -> Role:
        roles: list = await client.http.get(f"/guilds/{guild_id}/roles")

        for role in roles:
            if int(role['id']) == role_id:
                return cls.from_dict(role)
