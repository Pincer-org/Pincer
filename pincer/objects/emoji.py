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
from typing import Optional, List

from .role import Role
from .user import User
from ..utils import APIObject, APINullable, MISSING, Snowflake


@dataclass
class Emoji(APIObject):
    """
    :param id:
        emoji id

    :param name:
        emoji name

    :param animated:
        whether this emoji is animated

    :param available:
        whether this emoji can be used, may be false due to loss of Server
        Boosts

    :param managed:
        whether this emoji is managed

    :param require_colons:
        whether this emoji must be wrapped in colons

    :param roles:
        roles allowed to use this emoji

    :param user:
        user that created this emoji
    """

    id: Optional[Snowflake]
    name: Optional[str]

    animated: APINullable[bool] = MISSING
    available: APINullable[bool] = MISSING
    managed: APINullable[bool] = MISSING
    require_colons: APINullable[bool] = MISSING
    roles: APINullable[List[Role]] = MISSING
    user: APINullable[User] = MISSING
