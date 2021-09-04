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
from typing import Optional

from pincer.objects.user import User
from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, OptionallyProvided


class StickerType(Enum):
    STANDARD = 1
    GUILD = 2


class StickerFormatType(Enum):
    PNG = 1
    APNG = 2
    LOTTIE = 3


@dataclass
class Sticker(APIObject):
    description: Optional[str]
    format_type: StickerFormatType
    id: int
    name: str
    tags: str
    type: StickerType

    available: OptionallyProvided[bool] = MISSING
    guild_id: OptionallyProvided[int] = MISSING
    pack_id: OptionallyProvided[int] = MISSING
    sort_value: OptionallyProvided[int] = MISSING
    user: OptionallyProvided[User] = MISSING
