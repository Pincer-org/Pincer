from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..user.user import User as User
from typing import List, Optional

class Application(APIObject, GuildProperty):
    bot_public: bool
    bot_require_code_grant: bool
    description: str
    id: Snowflake
    icon: Optional[str]
    name: str
    privacy_policy_url: APINullable[str]
    summary: str
    verify_key: str
    cover_image: APINullable[str]
    flags: APINullable[int]
    guild_id: APINullable[Snowflake]
    owner: APINullable[User]
    primary_sku_id: APINullable[Snowflake]
    rpc_origins: APINullable[List[str]]
    slug: APINullable[str]
    terms_of_service_url: APINullable[str]
