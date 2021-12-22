from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.conversion import construct_client_dict as construct_client_dict
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.guild import Guild as Guild
from ..guild.member import GuildMember as GuildMember
from ..guild.role import Role as Role
from ..message.emoji import Emoji as Emoji
from ..message.sticker import Sticker as Sticker
from ..user import User as User
from .presence import PresenceUpdateEvent as PresenceUpdateEvent
from typing import Any, List, Optional

class GuildBanAddEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    user: User

class GuildBanRemoveEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    user: User

class GuildEmojisUpdateEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    emojis: List[Emoji]

class GuildStickersUpdateEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    stickers: List[Sticker]

class GuildIntegrationsUpdateEvent(APIObject, GuildProperty):
    guild_id: Snowflake

class GuildMemberAddEvent(GuildMember, GuildProperty):
    guild_id: Snowflake

class GuildMemberRemoveEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    user: User
    def __post_init__(self) -> None: ...

class GuildMemberUpdateEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    roles: List[Snowflake]
    user: User
    nick: APINullable[Optional[str]]
    joined_at: Optional[Timestamp]
    premium_since: APINullable[Optional[Timestamp]]
    deaf: APINullable[bool]
    mute: APINullable[bool]
    pending: APINullable[bool]
    def __post_init__(self) -> None: ...

class GuildMembersChunkEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    members: List[GuildMember]
    chunk_index: int
    chunk_count: int
    not_found: APINullable[List[Any]]
    presences: APINullable[PresenceUpdateEvent]
    nonce: APINullable[str]
    def __post_init__(self) -> None: ...

class GuildRoleCreateEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    role: Role

class GuildRoleUpdateEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    role: Role

class GuildRoleDeleteEvent(APIObject, GuildProperty):
    guild_id: Snowflake
    role_id: Snowflake

class GuildStatusEvent(APIObject):
    guild: Guild
    online: int
