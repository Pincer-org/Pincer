from ...utils.api_object import APIObject as APIObject, MISSING as MISSING
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable
from ..guild.stage import PrivacyLevel as PrivacyLevel
from ..user.user import User as User
from enum import IntEnum
from typing import Optional

class EventStatus(IntEnum):
    SCHEDULED: int
    ACTIVE: int
    COMPLETED: int
    CANCELLED: int

class GuildScheduledEventEntityType(IntEnum):
    STAGE_INSTANCE: int
    VOICE: int
    EXTERNAL: int

class ScheduledEvent(APIObject):
    id: Snowflake
    name: str
    guild_id: Snowflake
    scheduled_start_time: Timestamp
    privacy_level: PrivacyLevel
    status: EventStatus
    entity_type: GuildScheduledEventEntityType
    channel_id: APINullable[Snowflake]
    creator_id: APINullable[Snowflake]
    scheduled_end_time: Optional[Timestamp]
    description: APINullable[str]
    entity_id: APINullable[Snowflake]
    entity_metadata: APINullable[str]
    creator: APINullable[User]
    user_count: APINullable[int]
