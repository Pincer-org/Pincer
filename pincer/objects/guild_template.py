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

from .guild import Guild
from .user import User
from ..utils import APIObject, Snowflake, Timestamp


@dataclass
class GuildTemplate(APIObject):
    """
    Represents a code that when used,
    creates a guild based on a snapshot of an existing guild.

    :param code:
        the template code (unique ID)

    :param name:
        template name

    :param description:
        the description for the template

    :param usage_count:
        number of times this template has been used

    :param creator_id:
        the ID of the user who created the template

    :param creator: the
        user who created the template

    :param created_at:
        when this template was created

    :param updated_at:
        when this template was last synced to the source guild

    :param source_guild_id:
        the ID of the guild this template is based on

    :param serialized_source_guild:
        the guild snapshot this template contains

    :param is_dirty:
        whether the template has unsynced changes
    """
    code: str
    name: str
    description: Optional[str]
    usage_count: int
    creator_id: Snowflake
    creator: User
    created_at: Timestamp
    updated_at: Timestamp
    source_guild_id: Snowflake
    serialized_source_guild: Guild
    is_dirty: Optional[bool]
