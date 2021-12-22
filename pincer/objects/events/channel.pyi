from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING

class ChannelPinsUpdateEvent(APIObject, ChannelProperty, GuildProperty):
    channel_id: Snowflake
    guild_id: APINullable[Snowflake]
    last_pin_timestamp: APINullable[Timestamp]
