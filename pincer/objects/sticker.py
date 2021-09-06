# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from pincer.objects.user import User
from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, APINullable
from pincer.utils.snowflake import Snowflake


class StickerType(Enum):
    """
    Displays from where the sticker comes from.

    :param STANDARD:
        Sticker is included in the default Discord sticker pack.

    :param GUILD:
        Sticker is a custom sticker from a discord server.
    """
    STANDARD = 1
    GUILD = 2


class StickerFormatType(Enum):
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
        for guild stickers, the Discord name of a unicode emoji representing
        the sticker's expression. for standard stickers, a comma-separated list
        of related expressions.

    :param type:
        type of sticker

    :param available:
        whether this guild sticker can be used, may be false due to loss of
        Server Boosts

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
