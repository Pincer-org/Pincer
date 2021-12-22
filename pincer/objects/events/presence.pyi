from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..user.user import User as User
from enum import IntEnum
from typing import Any, List, Optional, Tuple

class ActivityType(IntEnum):
    GAME: int
    STREAMING: int
    LISTENING: int
    WATCHING: int
    CUSTOM: int
    COMPETING: int

class ActivityTimestamp(APIObject):
    start: APINullable[int]
    end: APINullable[int]

class ActivityEmoji(APIObject):
    name: str
    id: APINullable[Snowflake]
    animated: APINullable[bool]

class ActivityParty(APIObject):
    id: APINullable[str]
    size: APINullable[Tuple[int, int]]

class ActivityAssets(APIObject):
    large_image: APINullable[str]
    large_text: APINullable[str]
    small_image: APINullable[str]
    small_text: APINullable[str]

class ActivitySecrets(APIObject):
    join: APINullable[str]
    spectate: APINullable[str]
    match_: APINullable[str]

class ActivityFlags(IntEnum):
    INSTANCE: Any
    JOIN: Any
    SPECTATE: Any
    JOIN_REQUEST: Any
    SYNC: Any
    PLAY: Any

class ActivityButton(APIObject):
    label: str
    url: str

class Activity(APIObject):
    name: str
    type: ActivityType
    created_at: int
    url: APINullable[Optional[str]]
    timestamps: APINullable[ActivityTimestamp]
    application_id: APINullable[Snowflake]
    details: APINullable[Optional[str]]
    state: APINullable[Optional[str]]
    emoji: APINullable[Optional[ActivityEmoji]]
    party: APINullable[ActivityParty]
    assets: APINullable[ActivityAssets]
    secrets: APINullable[ActivitySecrets]
    instance: APINullable[bool]
    flags: APINullable[ActivityFlags]
    buttons: APINullable[List[ActivityButton]]

class ClientStatus(APIObject):
    desktop: APINullable[str]
    mobile: APINullable[str]
    web: APINullable[str]

class PresenceUpdateEvent(APIObject, GuildProperty):
    user: User
    status: str
    activities: List[Activity]
    client_status: ClientStatus
    guild_id: APINullable[Snowflake]
