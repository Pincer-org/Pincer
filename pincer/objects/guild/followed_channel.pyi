from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty
from ...utils.snowflake import Snowflake as Snowflake

class FollowedChannel(APIObject, ChannelProperty):
    channel_id: Snowflake
    webhook_id: Snowflake
