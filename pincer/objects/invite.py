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
from typing import Optional, List

from pincer.utils.api_object import APIObject

from pincer.objects.channel import Channel
from pincer.objects.guild import Guild
from pincer.objects.user import User
from pincer.objects.member import Member
from pincer.objects.application import Application
from pincer.utils.constants import APINullable, MISSING
from pincer.utils.timestamp import Timestamp


class InviteTargetType(Enum):
    STREAM = 1
    EMBEDDED_APPLICATION = 2


@dataclass
class InviteStageInstance(APIObject):
    members: List[Member]
    participant_count: int
    speaker_count: int
    topic: str

@dataclass
class InviteMetadata(APIObject):
    """Extra information about an invite, will extend the invite object.


    :param uses:
        number of times this invite has been used

    :param max_uses:
        max number of times this invite can be used

    :param max_age:
        duration (in seconds) after which the invite expires

    :param temporary:
        whether this invite only grants temporary membership

    :param created_at:
        when this invite was created
    """
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: Timestamp

@dataclass
class Invite(APIObject):
    channel: Channel
    code: str

    approximate_member_count: APINullable[int] = MISSING
    approximate_presence_count: APINullable[int] = MISSING
    expires_at: APINullable[Optional[Timestamp]] = MISSING
    inviter: APINullable[User] = MISSING
    guild: APINullable[Guild] = MISSING
    stage_instance: APINullable[InviteStageInstance] = MISSING
    target_type: APINullable[InviteTargetType] = MISSING
    target_user: APINullable[User] = MISSING
    target_application: APINullable[Application] = MISSING
