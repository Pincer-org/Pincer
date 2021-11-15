# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils import APIObject

if TYPE_CHECKING:
    from typing import Optional

    from ..guild import Guild
    from ..user.user import User
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp


@dataclass
class GuildTemplate(APIObject):
    """Represents a code that when used,
    creates a guild based on a snapshot of an existing guild.

    Attributes
    ----------
    code: :class:`str`
        the template code (unique ID)
    name: :class:`str`
        template name
    description: Optional[:class:`str`]
        the description for the template
    usage_count: :class:`int`
        number of times this template has been used
    creator_id: :class:`~pincer.utils.snowflake.Snowflake`
        the ID of the user who created the template
    creator: :class:`~pincer.objects.user.user.User`
        user who created the template
    created_at: :class:`~pincer.utils.timestamp.Timestamp`
        when this template was created
    updated_at: :class:`~pincer.utils.timestamp.Timestamp`
        when this template was last synced to the source guild
    source_guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        the ID of the guild this template is based on
    serialized_source_guild: :class:`~pincer.objects.guild.guild.Guild`
        the guild snapshot this template contains
    is_dirty: Optional[:class:`bool`]
        whether the template has unsynced changes
    """
    code: str
    name: str
    description: Optional[str]
    usage_count: int
    creator_id: Snowflake
    creator: User
    created_at: Timestamp
    updated_at: Timestamp
    source_guild_id: Snowflake
    serialized_source_guild: Guild
    is_dirty: Optional[bool]
