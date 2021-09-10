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
from enum import IntEnum
from typing import Optional

from ..utils import APIObject, APINullable, MISSING, Snowflake, convert


class PremiumTypes(IntEnum):
    """
    The type of Discord premium a user has.
    """
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class VisibilityType(IntEnum):
    """
    The type of a connection visibility.
    """
    NONE = 0
    EVERYONE = 1


@dataclass
class User(APIObject):
    """
    Represents a Discord user. This can be a bot account or a
    human account.

    :param avatar:
        the user's avatar hash

    :param discriminator:
        the user's 4-digit discord-tag

    :param flags:
        the flags on a user's account

    :param id:
        the user's id

    :param username:
        the user's username, not unique across the platform

    :param accent_color:
        the user's banner color encoded as an integer representation of
        hexadecimal color code

    :param banner:
        the user's banner, or null if unset

    :param bot:
        whether the user belongs to an OAuth2 application

    :param email:
        the user's email

    :param locale:
        the user's chosen language option

    :param mfa_enabled:
        whether the user has two factor enabled on their account

    :param premium_type:
        the type of Nitro subscription on a user's account

    :param public_flags:
        the public flags on a user's account

    :param system:
        whether the user is an Official Discord System user (part of the urgent
        message system)

    :param verified:
        whether the email on this account has been verified
    """

    avatar: Optional[str]
    discriminator: str
    id: Snowflake
    username: str

    flags: APINullable[int] = MISSING
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
    def premium(self) -> APINullable[PremiumTypes]:
        """
        The user their premium type in a usable enum.
        """
        return MISSING \
            if self.premium_type is MISSING \
            else PremiumTypes(self.premium_type)

    def __str__(self):
        """Return the discord tag when object gets used as a string."""
        return self.username + '#' + self.discriminator

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)
