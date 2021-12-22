from ...utils.api_object import APIObject as APIObject
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..app.application import Application as Application
from ..guild.guild import Guild as Guild
from ..user.user import User as User
from typing import List, Tuple

class HelloEvent(APIObject):
    heartbeat_interval: int

class ReadyEvent(APIObject):
    v: int
    user: User
    guilds: List[Guild]
    session_id: str
    application: Application
    shard: APINullable[Tuple[int, int]]
