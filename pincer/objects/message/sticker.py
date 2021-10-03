# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from ..user import User
from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils import APINullable, Snowflake


class StickerType(IntEnum):
    """
    Displays from where the sticker comes from.

    :param STANDARD:
        Sticker is included in the default Discord sticker pack.

    :param GUILD:
        Sticker is a custom sticker from a discord server.
    """
    STANDARD = 1
    GUILD = 2


class StickerFormatType(IntEnum):
    """
    The type of the sticker.

    :param PNG:
        Sticker is of PNG format.

    :param APNG:
        Sticker is animated with APNG format.

    :param LOTTIE:
        Sticker is animated with with LOTTIE format. (vector based)
    """
    PNG = 1
    APNG = 2
    LOTTIE = 3


@dataclass
class Sticker(APIObject):
    """
    Represents a Discord sticker.

    :param description:
        description of the sticker

    :param format_type:
        type of sticker format

    :param id:
        id of the sticker

    :param name:
        name of the sticker

    :param tags:
        for guild stickers, the Discord name of a unicode emoji
        representing the sticker's expression. For standard stickers,
        a comma-separated list of related expressions.

    :param type:
        type of sticker

    :param available:
        whether this guild sticker can be used,
        may be false due to loss of Server Boosts

    :param guild_id:
        id of the guild that owns this sticker

    :param pack_id:
        for standard stickers, id of the pack the sticker is from

    :param sort_value:
        the standard sticker's sort order within its pack

    :param user:
        the user that uploaded the guild sticker
    """

    description: Optional[str]
    format_type: StickerFormatType
    id: Snowflake
    name: str
    tags: str
    type: StickerType

    available: APINullable[bool] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    pack_id: APINullable[Snowflake] = MISSING
    sort_value: APINullable[int] = MISSING
    user: APINullable[User] = MISSING


@dataclass
class StickerItem(APIObject):
    """
    Represents the smallest amount of data required to render a sticker.
    A partial sticker object.

    :param id:
        id of the sticker

    :param name:
        name of the sticker

    :param format_type:
        type of sticker format
    """

    id: Snowflake
    name: str
    format_type: StickerFormatType


@dataclass
class StickerPack(APIObject):
    """
    Represents a pack of standard stickers.

    :param id:
        id of the sticker pack

    :param stickers:
        the stickers in the pack

    :param name:
        name of the sticker pack

    :param sku_id:
        id of the pack's SKU

    :param description:
        description of the sticker pack

    :param cover_sticker_id:
        id of a sticker in the pack which is shown as the pack's icon

    :param banner_asset_id:
        id of the sticker pack's banner image
    """

    id: Snowflake
    stickers: List[Sticker]
    name: str
    sku_id: Snowflake
    description: str

    cover_sticker_id: APINullable[Snowflake] = MISSING
    banner_asset_id: APINullable[Snowflake] = MISSING
