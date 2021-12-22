from ...utils.api_object import APIObject as APIObject, ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.member import GuildMember as GuildMember
from ..message.emoji import Emoji as Emoji
from typing import List

class MessageDeleteEvent(APIObject, ChannelProperty, GuildProperty):
    id: Snowflake
    channel_id: Snowflake
    guild_id: APINullable[Snowflake]

class MessageDeleteBulkEvent(APIObject, ChannelProperty, GuildProperty):
    ids: List[Snowflake]
    channel_id: Snowflake
    guild_id: APINullable[Snowflake]

class MessageReactionAddEvent(APIObject, ChannelProperty, GuildProperty):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji
    guild_id: APINullable[Snowflake]
    member: APINullable[GuildMember]

class MessageReactionRemoveEvent(APIObject, ChannelProperty, GuildProperty):
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji
    guild_id: APINullable[Snowflake]

class MessageReactionRemoveAllEvent(APIObject, ChannelProperty, GuildProperty):
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: APINullable[Snowflake]

class MessageReactionRemoveEmojiEvent(APIObject, ChannelProperty, GuildProperty):
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji
    guild_id: APINullable[Snowflake]
