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
from typing import Optional

from pincer.objects.member import Member
from pincer.utils.api_object import APIObject
from pincer.utils.snowflake import Snowflake
from pincer.utils.constants import MISSING, APINullable
from pincer.utils.timestamp import Timestamp

@dataclass
class VoiceState(APIObject):
    """
    Used to represent a user's voice connection status

    :param guild_id:
        the guild id this voice state is for

    :param channel_id:
        the channel id this user is connected to

    :param user_id:
        the user id this voice state is for

    :param member:
        the guild member this voice state is for

    :param session_id:
        the session id for this voice state

    :param deaf:
        whether this user is deafened by the server

    :param mute:
        whether this user is muted by the server

    :param self_deaf:
        whether this user is locally deafened

    :param self_mute:
        whether this user is locally muted

    :param self_stream:
        whether this user is streaming using "Go Live"

    :param self_video:
        whether this user's camera is enabled

    :param suppress:
        whether this user is muted by the current user

    :param request_to_speak_timestamp:
        the time at which the user requested to speak
    """
    channel_id: Optional[Snowflake]
    user_id: Snowflake
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: Optional[Timestamp]

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[Member] = MISSING
    self_stream: APINullable[bool] = MISSING
