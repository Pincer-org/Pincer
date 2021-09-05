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

from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, APINullable
from pincer.utils.snowflake import Snowflake


class PremiumTypes(Enum):
    # TODO: Write documentation
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


@dataclass
class User(APIObject):
    # TODO: Write documentation
    avatar: Optional[str]
    discriminator: str
    flags: int
    id: Snowflake
    username: str

    accent_color: APINullable[Optional[int]] = MISSING
    banner: APINullable[Optional[str]] = MISSING
    bot: APINullable[bool] = MISSING
    email: APINullable[Optional[str]] = MISSING
    locale: APINullable[str] = MISSING
    mfa_enabled: APINullable[bool] = MISSING
    premium_type: APINullable[int] = MISSING
    public_flags: APINullable[int] = MISSING
    system: APINullable[bool] = MISSING
    verified: APINullable[bool] = MISSING

    @property
    def premium(self) -> PremiumTypes:
        # TODO: Write documentation
        return PremiumTypes(self.premium_type)

    @property
    def user(self) -> str:
        """
        :return:
            Return the full discord tag of the client.
        """
        return self.username + '#' + self.discriminator

    def __str__(self):
        """return the discord tag when object gets used as a string."""
        return self.user
