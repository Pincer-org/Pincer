from ...utils.api_object import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING

class ThreadMetadata(APIObject):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: Timestamp
    locked: bool
    invitable: APINullable[bool]

class ThreadMember(APIObject):
    join_timestamp: Timestamp
    flags: int
    id: APINullable[Snowflake]
    user_id: APINullable[Snowflake]
