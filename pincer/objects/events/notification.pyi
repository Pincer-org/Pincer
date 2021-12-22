from ...objects.message import UserMessage as UserMessage
from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty
from ...utils.snowflake import Snowflake as Snowflake

class NotificationCreateEvent(APIObject, ChannelProperty):
    channel_id: Snowflake
    message: UserMessage
    icon_url: str
    title: str
    body: str
