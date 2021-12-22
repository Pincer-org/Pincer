from ...utils.api_object import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from .user import User as User
from enum import IntEnum
from typing import Optional

class IntegrationExpireBehavior(IntEnum):
    REMOVE_ROLE: int
    KICK: int

class IntegrationAccount(APIObject):
    id: str
    name: str

class IntegrationApplication(APIObject):
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    summary: str
    bot: APINullable[User]

class Integration(APIObject):
    id: Snowflake
    name: str
    type: str
    enabled: bool
    account: IntegrationAccount
    syncing: APINullable[bool]
    role_id: APINullable[Snowflake]
    enable_emoticons: APINullable[bool]
    expire_behavior: APINullable[IntegrationExpireBehavior]
    expire_grace_period: APINullable[int]
    user: APINullable[User]
    synced_at: APINullable[Timestamp]
    subscriber_count: APINullable[int]
    revoked: APINullable[bool]
    application: APINullable[IntegrationApplication]
