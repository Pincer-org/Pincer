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
    # Note: Current docs are mostly copied from
    # https://discord.com/developers/docs/resources/user

    id: int #: The user's id
    flags: int #: The flags on a user's account
    username: str #: The user's username, not unique across the platform
    discriminator: str #: The user's 4-digit discord-tag
    bot: Optional[bool] = False #: Whether the user is a bot
    email: Optional[str] = None #: The user's email
    banner: Optional[str] = None #: The user's banner (if exists)
    locale: Optional[str] = None #: The user's chosen language
    avatar: Optional[str] = None #: The user's avatar hash
    system: Optional[bool] = False #: Whether user is an Official Discord System user
    accent_color: Optional[int] = 0 #: The user's banner hexadecimal color code as an integer
    public_flags: Optional[int] = 0 #: The public flags on the account
    verified: Optional[bool] = False #: Whether the email on this account has been verified
    avatar_url: Optional[str] = None #: The url to the user's avatar
    mfa_enabled: Optional[bool] = False #: Whether the user has two factor enabled on their account
    premium_type: Optional[PremiumTypes] = PremiumTypes.NONE #: The type of Nitro subscription on a user's account

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
        """
        :return:
            Return the full discord tag of the client.
        """
        return self.username + '#' + self.discriminator

    def __str__(self):
        """Return the discord tag when object gets used as a string."""
        return self.user
