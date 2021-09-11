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
from typing import List

from ..objects.channel import Channel
from ..objects.thread import ThreadMember
from ..utils import APIObject, APINullable, MISSING, Snowflake

@dataclass
class ThreadListSyncEvent(APIObject):
    """
    Sent when the current user gains access to a channel.

    :param guild_id:
        the id of the guild

    :param channel_ids:
        the parent channel ids whose threads are being synced.
        If omitted, then threads were synced for the entire guild.
        This array may contain channel_ids that have no active
        threads as well, so you know to clear that data.

    :param threads:
        all active threads in the given channels that
        the current user can access

    :param members:
        all thread member objects from the synced threads for
        the current user, indicating which threads the current
        user has been added to
    """
    guild_id: Snowflake
    threads: List[Channel]
    members: List[ThreadMember]

    channel_ids: APINullable[List[Snowflake]] = MISSING

@dataclass
class ThreadMembersUpdateEvent(APIObject):
    """
    Sent when anyone is added to or removed from a thread.
    If the current user does not have the `GUILD_MEMBERS`
    Gateway Intent, then this event will only be sent if
    the current user was added to or removed from the thread.

    :param id:
        the id of the thread

    :param guild_id:
        the id of the guild

    :param member_count:
        the approximate number of members in the thread, capped at 50

    :param added_members:
        the users who were added to the thread

    :param removed_member_ids:
        the id of the users who were removed from the thread
    """
    id: Snowflake
    guild_id: Snowflake
    member_count: int

    added_members: APINullable[List[ThreadMember]] = MISSING
    removed_member_ids: APINullable[List[Snowflake]] = MISSING