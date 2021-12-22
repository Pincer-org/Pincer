from ...client import Client as Client
from ...utils.api_object import APIObject as APIObject
from ...utils.conversion import construct_client_dict as construct_client_dict
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..user.user import User as User
from typing import List, Optional

class BaseMember(APIObject):
    joined_at: APINullable[Timestamp]
    roles: APINullable[List[Snowflake]]
    deaf: bool
    mute: bool
    hoisted_role: APINullable[Snowflake]

class PartialGuildMember(APIObject):
    id: Snowflake
    username: str
    discriminator: str
    avatar: str
    public_flags: int
    member: Optional[BaseMember]

class GuildMember(BaseMember, User, APIObject):
    nick: APINullable[Optional[str]]
    pending: APINullable[bool]
    is_pending: APINullable[bool]
    permissions: APINullable[str]
    premium_since: APINullable[Optional[Timestamp]]
    user: APINullable[User]
    avatar: APINullable[str]
    def __post_init__(self) -> None: ...
    def set_user_data(self, user: User): ...
    @classmethod
    async def from_id(cls, client: Client, guild_id: int, user_id: int) -> GuildMember: ...
