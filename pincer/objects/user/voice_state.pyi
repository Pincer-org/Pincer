from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.member import GuildMember as GuildMember

class VoiceState(APIObject, ChannelProperty, GuildProperty):
    user_id: Snowflake
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_video: bool
    suppress: bool
    channel_id: APINullable[Snowflake]
    request_to_speak_timestamp: APINullable[Timestamp]
    guild_id: APINullable[Snowflake]
    member: APINullable[GuildMember]
    self_stream: APINullable[bool]
