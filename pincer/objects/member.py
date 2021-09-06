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

from pincer.utils.api_object import APIObject
from pincer.objects.user import User
from pincer.utils.constants import APINullable, MISSING
from pincer.utils.snowflake import Snowflake
from pincer.utils.timestamp import Timestamp


@dataclass
class GuildMember(APIObject):
    """
    Represents a member which resides in a guild/server.
    
    :param deaf:
        whether the user is deafened in voice channels

    :param joined_at:
        when the user joined the guild

    :param mute:
        whether the user is muted in voice channels

    :param roles:
        array of role object ids

    :param nick:
        this users guild nickname

    :param pending:
        whether the user has not yet passed the guild's Membership Screening
        requirements

    :param permissions:
        total permissions of the member in the channel, including overwrites,
        returned when in the interaction object

    :param premium_since:
        when the user started boosting the guild

    :param user:
        the user this guild member represents
    """

    deaf: bool
    joined_at: Timestamp
    mute: bool
    roles: List[Snowflake]

    nick: APINullable[Optional[str]] = MISSING
    pending: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_since: APINullable[Optional[Timestamp]] = MISSING
    user: APINullable[User] = MISSING
