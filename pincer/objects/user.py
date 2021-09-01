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
from typing import Optional, Union

from websockets.typing import Data


class PremiumTypes(Enum):
    # TODO: Write documentation
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


@dataclass
class User:
    # TODO: Write documentation
    id: int
    flags: int
    username: str
    discriminator: str
    bot: Optional[bool] = False
    email: Optional[str] = None
    banner: Optional[str] = None
    locale: Optional[str] = None
    avatar: Optional[str] = None
    system: Optional[bool] = False
    accent_color: Optional[int] = 0
    public_flags: Optional[int] = 0
    verified: Optional[bool] = False
    avatar_url: Optional[str] = None
    mfa_enabled: Optional[bool] = False
    premium_type: Optional[int] = 0

    @classmethod
    def from_dict(cls, data: Data[str, Union[str, bool, int]]) -> User:
        # TODO: Write documentation
        return cls(**data)

    @property
    def premium(self) -> PremiumTypes:
        # TODO: Write documentation
        return PremiumTypes(self.premium_type)

    @property
    def user(self) -> str:
        # TODO: Write documentation
        return self.username + '#' + self.discriminator

    def __str__(self):
        # Lets return the user#discriminator when the object gets used
        # as a string.
        return self.user
