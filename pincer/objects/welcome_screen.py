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

from ..utils import APIObject, Snowflake


@dataclass
class WelcomeScreenChannel(APIObject):
    """
    Represents a welcome screen channel. This is a channel which gets
    shown on the welcome screen.

    :param channel_id:
        the channel's id

    :param description:
        the description shown for the channel

    :param emoji_id:
        the emoji id, if the emoji is custom

    :param emoji_name:
        the emoji name if custom, the unicode character if standard, or null if
        no emoji is set
    """

    channel_id: Snowflake
    description: str

    emoji_id: Optional[int] = None
    emoji_name: Optional[str] = None


@dataclass
class WelcomeScreen(APIObject):
    """
    Representation of a Discord guild/server welcome screen.

    :description:
        the server description shown in the welcome screen

    :welcome_channels:
        the channels shown in the welcome screen, up to 5
    """
    welcome_channels: List[WelcomeScreenChannel]

    description: Optional[str] = None
