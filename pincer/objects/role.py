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

from ..utils import APIObject, APINullable, MISSING, Snowflake


@dataclass
class RoleTags(APIObject):
    """
    Special tags/flags which have been defined for a role.

    :bot_id:
        The id of the bot this role belongs to.
        (the role got created by adding the bot with this id)

    :integration_id:
        The id of the integration this role belongs to.
        (the role got created by adding an integration with this id)

    :premium_subscriber:
        Whether this is the guild's premium subscriber role or not.
    """
    bot_id: APINullable[Snowflake] = MISSING
    integration_id: APINullable[Snowflake] = MISSING
    premium_subscriber: APINullable[bool] = MISSING


@dataclass
class Role(APIObject):
    """
    Represents a Discord guild/server role.

    :param color:
        integer representation of hexadecimal color code

    :param hoist:
        if this role is pinned in the user listing

    :param id:
        role id

    :param managed:
        whether this role is managed by an integration

    :param mentionable:
        whether this role is mentionable

    :param name:
        role name

    :param permissions:
        permission bit set

    :param position:
        position of this role

    :param tags:
        the tags this role has
    """

    color: int
    hoist: bool
    id: Snowflake
    managed: bool
    mentionable: bool
    name: str
    permissions: str
    position: int

    tags: APINullable[RoleTags] = MISSING
