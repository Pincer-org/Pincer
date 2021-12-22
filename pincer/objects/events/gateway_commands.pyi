from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..app.intents import Intents as Intents
from .presence import Activity as Activity
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

class Identify(APIObject):
    token: str
    properties: Dict[str, str]
    intents: Intents
    compress: APINullable[bool]
    large_threshold: APINullable[int]
    shard: APINullable[Tuple[int, int]]
    presence: APINullable[Any]

class Resume(APIObject):
    token: str
    session_id: str
    seq: int

class RequestGuildMembers(APIObject, GuildProperty):
    guild_id: Snowflake
    limit: int
    query: APINullable[str]
    presences: APINullable[bool]
    user_ids: APINullable[Union[Snowflake, List[Snowflake]]]
    nonce: APINullable[str]

class UpdateVoiceState(APIObject, GuildProperty):
    guild_id: Snowflake
    self_mute: bool
    self_deaf: bool
    channel_id: Optional[Snowflake]

class StatusType(Enum):
    online: Any
    dnd: Any
    idle: Any
    invisible: Any
    offline: Any

class UpdatePresence(APIObject):
    activities: List[Activity]
    status: StatusType
    afk: bool
    since: Optional[int]
