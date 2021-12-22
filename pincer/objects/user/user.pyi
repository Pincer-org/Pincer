from ...client import Client as Client
from ...objects.message.user_message import UserMessage as UserMessage
from ...utils.api_object import APIObject as APIObject
from ...utils.color import Color as Color
from ...utils.conversion import construct_client_dict as construct_client_dict
from ...utils.convert_message import MessageConvertable as MessageConvertable
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..guild import channel as channel
from PIL import Image
from enum import IntEnum
from typing import Optional

PILLOW_IMPORT: bool

class PremiumTypes(IntEnum):
    NONE: int
    NITRO_CLASSIC: int
    NITRO: int

class VisibilityType(IntEnum):
    NONE: int
    EVERYONE: int

class User(APIObject):
    id: APINullable[Snowflake]
    username: APINullable[str]
    discriminator: APINullable[str]
    avatar: APINullable[str]
    flags: APINullable[int]
    accent_color: APINullable[Optional[int]]
    banner: APINullable[Optional[str]]
    banner_color: APINullable[Optional[Color]]
    bot: APINullable[bool]
    email: APINullable[Optional[str]]
    locale: APINullable[str]
    mfa_enabled: APINullable[bool]
    premium_type: APINullable[int]
    public_flags: APINullable[int]
    system: APINullable[bool]
    verified: APINullable[bool]
    @property
    def premium(self) -> APINullable[PremiumTypes]: ...
    @property
    def mention(self) -> str: ...
    def get_avatar_url(self, size: int = ..., ext: str = ...) -> str: ...
    async def get_avatar(self, size: int = ..., ext: str = ...) -> Image: ...
    @classmethod
    async def from_id(cls, client: Client, user_id: int) -> User: ...
    async def get_dm_channel(self) -> channel.Channel: ...
    async def send(self, message: MessageConvertable) -> UserMessage: ...
