from ...utils.api_object import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from typing import Optional

class GuildWidget(APIObject):
    enabled: bool
    channel_id: Optional[Snowflake]
