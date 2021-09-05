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
from pincer.utils.constants import OptionallyProvided, MISSING
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
class Invite(APIObject):
    channel: Channel
    code: str

    approximate_member_count: OptionallyProvided[int] = MISSING
    approximate_presence_count: OptionallyProvided[int] = MISSING
    expires_at: OptionallyProvided[Optional[Timestamp]] = MISSING
    inviter: OptionallyProvided[User] = MISSING
    guild: OptionallyProvided[Guild] = MISSING
    stage_instance: OptionallyProvided[InviteStageInstance] = MISSING
    target_type: OptionallyProvided[InviteTargetType] = MISSING
    target_user: OptionallyProvided[User] = MISSING
    target_application: OptionallyProvided[Application] = MISSING
