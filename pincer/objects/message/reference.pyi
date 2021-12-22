from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING

class MessageReference(APIObject, ChannelProperty, GuildProperty):
    message_id: APINullable[Snowflake]
    channel_id: APINullable[Snowflake]
    guild_id: APINullable[Snowflake]
    fail_if_not_exists: APINullable[bool]
