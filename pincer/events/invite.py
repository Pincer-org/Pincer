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

from dataclasses import dataclass

from ..objects.invite import InviteTargetType
from ..objects.user import User
from ..utils.api_object import APIObject
from ..utils.snowflake import Snowflake
from ..utils.timestamp import Timestamp
from ..utils.types import APINullable, MISSING

@dataclass
class InviteCreateEvent(APIObject):
    """
    Sent when a new invite to a channel is created.

    :param channel_id:
        the channel the invite is for

    :param code:
        the unique invite code

    :param created_at:
        the time at which the invite was created

    :param guild_id:
        the guild of the invite

    :param inviter:
        the user that created the invite

    :param max_age:
        how long the invite is valid for (in seconds)

    :param max_uses:
        the maximum number of times the invite can be used

    :param target_type:
        the type of target for this voice channel invite

    :param target_user:
        the user whose stream to display for
        this voice channel stream invite

    :param target_application:
        the embedded application to open for this
        voice channel embedded application invite

    :param temporary:
        whether or not the invite is temporary (invited users will
        be kicked on disconnect unless they're assigned a role)

    :param uses:
        how many times the invite has been used (always will be 0)
    """
    channel_id: Snowflake
    code: str
    created_at: Timestamp
    max_age: int
    max_uses: int
    temporary: bool

    guild_id: APINullable[Snowflake] = MISSING
    inviter: APINullable[User] = MISSING
    target_type: APINullable[InviteTargetType] = MISSING
    target_user: APINullable[User] = MISSING
    uses: int = 0

@dataclass
class InviteDeleteEvent(APIObject):
    """
    Sent when an invite is deleted.

    :param channel_id:
        the channel of the invite

    :param guild_id:
        the guild of the invite

    :param code:
        the unique invite code
    """
    channel_id: Snowflake
    code: str

    guild_id: APINullable[Snowflake] = MISSING
