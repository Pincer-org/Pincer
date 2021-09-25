# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional

from .guild import Guild
from .user import User
from ..utils import APIObject, Snowflake, Timestamp


@dataclass
class GuildTemplate(APIObject):
    """
    Represents a code that when used,
    creates a guild based on a snapshot of an existing guild.

    :param code:
        the template code (unique ID)

    :param name:
        template name

    :param description:
        the description for the template

    :param usage_count:
        number of times this template has been used

    :param creator_id:
        the ID of the user who created the template

    :param creator: the
        user who created the template

    :param created_at:
        when this template was created

    :param updated_at:
        when this template was last synced to the source guild

    :param source_guild_id:
        the ID of the guild this template is based on

    :param serialized_source_guild:
        the guild snapshot this template contains

    :param is_dirty:
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
