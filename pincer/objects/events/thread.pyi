from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.channel import Channel as Channel
from ..guild.thread import ThreadMember as ThreadMember
from typing import List

class ThreadListSyncEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    threads: List[Channel]
    members: List[ThreadMember]
    channel_ids: APINullable[List[Snowflake]]

class ThreadMembersUpdateEvent(APIObject, GuildProperty):
    id: Snowflake
    guild_id: Snowflake
    member_count: int
    added_members: APINullable[List[ThreadMember]]
    removed_member_ids: APINullable[List[Snowflake]]
