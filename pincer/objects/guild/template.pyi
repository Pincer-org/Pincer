from ...utils import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ..guild import Guild as Guild
from ..user.user import User as User
from typing import Optional

class GuildTemplate(APIObject):
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
