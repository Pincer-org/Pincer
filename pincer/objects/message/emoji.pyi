from ...utils.api_object import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild.role import Role as Role
from ..user.user import User as User
from typing import List, Optional

class Emoji(APIObject):
    name: Optional[str]
    id: APINullable[Snowflake]
    animated: APINullable[bool]
    available: APINullable[bool]
    managed: APINullable[bool]
    require_colons: APINullable[bool]
    roles: APINullable[List[Role]]
    user: APINullable[User]
