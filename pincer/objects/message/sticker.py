# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List, Optional

    from ..user import User
    from ...utils import APINullable, Snowflake


class StickerType(IntEnum):
    """Displays from where the sticker comes from.

    Attributes
    ----------
    STANDARD:
        Sticker is included in the default Discord sticker pack.
    GUILD:
        Sticker is a custom sticker from a discord server.
    """
    STANDARD = 1
    GUILD = 2


class StickerFormatType(IntEnum):
    """The type of the sticker.

    Attributes
    ----------
    PNG:
        Sticker is of PNG format.
    APNG:
        Sticker is animated with APNG format.
    LOTTIE:
        Sticker is animated with with LOTTIE format. (vector based)
    """
    PNG = 1
    APNG = 2
    LOTTIE = 3


@dataclass
class Sticker(APIObject):
    """Represents a Discord sticker.

    Attributes
    ----------
    description: Optional[:class:`str`]
        description of the sticker
    format_type: :class:`~pincer.objects.message.sticker.StickerFormatType`
        type of sticker format
    id: :class:`~pincer.utils.snowflake.Snowflake`
        id of the sticker
    name: :class:`str`
        name of the sticker
    tags: :class:`str`
        for guild stickers, the Discord name of a unicode emoji
        representing the sticker's expression. For standard stickers,
        a comma-separated list of related expressions.
    type: :class:`~pincer.objects.message.sticker.StickerType`
        type of sticker
    available: APINullable[:class:`bool`]
        whether this guild sticker can be used,
        may be false due to loss of Server Boosts
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        id of the guild that owns this sticker
    pack_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        for standard stickers, id of the pack the sticker is from
    sort_value: APINullable[:class:`int`]
        the standard sticker's sort order within its pack
    user: APINullable[:class:`~pincer.objects.user.user.User`]
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
    """Represents the smallest amount of data required to render a sticker.
    A partial sticker object.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the sticker
    name: :class:`str`
        Name of the sticker
    format_type: :class:`~pincer.objects.message.sticker.StickerFormatType`
        Type of sticker format
    """

    id: Snowflake
    name: str
    format_type: StickerFormatType


@dataclass
class StickerPack(APIObject):
    """Represents a pack of standard stickers.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the sticker pack
    stickers: List[:class:`~pincer.objects.message.sticker.Sticker`]
        The stickers in the pack
    name: :class:`str`
        Name of the sticker pack
    sku_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the pack's SKU
    description: :class:`str`
        Description of the sticker pack
    cover_sticker_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of a sticker in the pack which is shown as the pack's icon
    banner_asset_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the sticker pack's banner image
    """

    id: Snowflake
    stickers: List[Sticker]
    name: str
    sku_id: Snowflake
    description: str

    cover_sticker_id: APINullable[Snowflake] = MISSING
    banner_asset_id: APINullable[Snowflake] = MISSING
