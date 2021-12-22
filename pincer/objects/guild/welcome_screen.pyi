from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty
from ...utils.snowflake import Snowflake as Snowflake
from typing import List, Optional

class WelcomeScreenChannel(APIObject, ChannelProperty):
    channel_id: Snowflake
    description: str
    emoji_id: Optional[int]
    emoji_name: Optional[str]

class WelcomeScreen(APIObject):
    welcome_channels: List[WelcomeScreenChannel]
    description: Optional[str]
