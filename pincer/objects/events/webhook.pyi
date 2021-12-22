from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty
from ...utils.snowflake import Snowflake as Snowflake

class WebhooksUpdateEvent(APIObject, ChannelProperty):
    guild_id: Snowflake
    channel_id: Snowflake
