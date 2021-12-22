from ...utils.api_object import APIObject as APIObject
from ...utils.timestamp import Timestamp as Timestamp
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..app.application import Application as Application
from ..guild.channel import Channel as Channel
from ..guild.member import GuildMember as GuildMember
from ..user.user import User as User
from .guild import Guild as Guild
from enum import IntEnum
from typing import List, Optional

class InviteTargetType(IntEnum):
    STREAM: int
    EMBEDDED_APPLICATION: int

class InviteStageInstance(APIObject):
    members: List[GuildMember]
    participant_count: int
    speaker_count: int
    topic: str

class Invite(APIObject):
    channel: Channel
    code: str
    approximate_member_count: APINullable[int]
    approximate_presence_count: APINullable[int]
    expires_at: APINullable[Optional[Timestamp]]
    inviter: APINullable[User]
    guild: APINullable[Guild]
    stage_instance: APINullable[InviteStageInstance]
    target_type: APINullable[InviteTargetType]
    target_user: APINullable[User]
    target_application: APINullable[Application]
    uses: APINullable[int]
    max_uses: APINullable[int]
    max_age: APINullable[int]
    temporary: APINullable[bool]
    created_at: APINullable[Timestamp]
    @property
    def link(self): ...
