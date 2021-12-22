from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from enum import Enum
from typing import Any, List, Optional

class VoiceServerUpdateEvent(APIObject, GuildProperty):
    token: str
    guild_id: Snowflake
    endpoint: Optional[str]

class VoiceChannelSelectEvent(APIObject, GuildProperty):
    channel_id: Optional[Snowflake]
    guild_id: Optional[Snowflake]

class VoiceConnectionStates(Enum):
    DISCONNECTED: Any
    AWAITING_ENDPOINT: Any
    AUTHENTICATING: Any
    CONNECTING: Any
    CONNECTED: Any
    VOICE_DISCONNECTED: Any
    VOICE_CONNECTING: Any
    VOICE_CONNECTED: Any
    NO_ROUTE: Any
    ICE_CHECKING: Any

class VoiceConnectionStatusEvent(APIObject):
    state: VoiceConnectionStates
    hostname: str
    pings: List[int]
    average_ping: int
    last_ping: int

class SpeakingStartEvent(APIObject):
    user_id: Snowflake

class SpeakingStopEvent(APIObject):
    user_id: Snowflake
