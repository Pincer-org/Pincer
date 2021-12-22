from ...utils import APINullable as APINullable, Snowflake as Snowflake
from ...utils.api_object import APIObject as APIObject
from ...utils.conversion import remove_none as remove_none
from ...utils.types import MISSING as MISSING
from ..user import User as User
from enum import IntEnum
from typing import List, Optional

class StickerType(IntEnum):
    STANDARD: int
    GUILD: int

class StickerFormatType(IntEnum):
    PNG: int
    APNG: int
    LOTTIE: int

class Sticker(APIObject):
    description: Optional[str]
    format_type: StickerFormatType
    id: Snowflake
    name: str
    tags: str
    type: StickerType
    available: APINullable[bool]
    guild_id: APINullable[Snowflake]
    pack_id: APINullable[Snowflake]
    sort_value: APINullable[int]
    user: APINullable[User]
    @classmethod
    async def from_id(cls, _id: Snowflake) -> Sticker: ...
    async def modify(self, name: Optional[str] = ..., description: Optional[str] = ..., tags: Optional[str] = ..., reason: Optional[str] = ...) -> Sticker: ...

class StickerItem(APIObject):
    id: Snowflake
    name: str
    format_type: StickerFormatType

class StickerPack(APIObject):
    id: Snowflake
    stickers: List[Sticker]
    name: str
    sku_id: Snowflake
    description: str
    cover_sticker_id: APINullable[Snowflake]
    banner_asset_id: APINullable[Snowflake]
