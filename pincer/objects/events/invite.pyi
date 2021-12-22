from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.invite import InviteTargetType as InviteTargetType
from ..user.user import User as User

class InviteCreateEvent(APIObject, ChannelProperty, GuildProperty):
    channel_id: Snowflake
    code: str
    created_at: Timestamp
    max_age: int
    max_uses: int
    temporary: bool
    guild_id: APINullable[Snowflake]
    inviter: APINullable[User]
    target_type: APINullable[InviteTargetType]
    target_user: APINullable[User]
    uses: int

class InviteDeleteEvent(APIObject, ChannelProperty, GuildProperty):
    channel_id: Snowflake
    code: str
    guild_id: APINullable[Snowflake]
