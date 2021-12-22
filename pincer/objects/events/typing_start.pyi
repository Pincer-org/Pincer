from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.member import GuildMember as GuildMember

class TypingStartEvent(APIObject, ChannelProperty, GuildProperty):
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int
    guild_id: APINullable[Snowflake]
    member: APINullable[GuildMember]
