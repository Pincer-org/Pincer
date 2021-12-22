from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from enum import IntEnum

class PrivacyLevel(IntEnum):
    PUBLIC: int
    GUILD_ONLY: int

class StageInstance(APIObject, ChannelProperty, GuildProperty):
    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable: bool
