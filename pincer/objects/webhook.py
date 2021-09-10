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

from .channel import Channel
from .guild import Guild
from .user import User
from ..utils import APIObject, APINullable, MISSING, Snowflake


class WebhookType(IntEnum):
    """
    Represents the type of a webhook.

    :param INCOMING:
        Incoming Webhooks can post messages to channels with a
        generated token.

    :param CHANNEL_FOLLOWER:
        Channel Follower Webhooks are internal webhooks used with
        Channel Following to post new messages into channels.

    :param APPLICATION:
        Application webhooks are webhooks used with Interactions
    """
    INCOMING = 1
    CHANNEL_FOLLOWER = 2
    APPLICATION = 3


@dataclass
class Webhook(APIObject):
    """
    Represents a Discord channel webhook.

    :param id:
        the id of the webhook

    :param type:
        the type of the webhook

    :param channel_id:
        the channel id this webhook is for, if any

    :param name:
        the default name of the webhook

    :param avatar:
        the default user avatar hash of the webhook

    :param application_id:
        the bot/OAuth2 application that created this webhook

    :param user:
        the user this webhook was created by (not returned when getting a
        webhook with its token)

    :param token:
        the secure token of the webhook (returned for Incoming Webhooks)

    :param source_guild:
        the guild of the channel that this webhook is following (returned for
        Channel Follower Webhooks)

    :param source_channel:
        the channel that this webhook is following (returned for Channel
        Follower Webhooks)

    :param url:
        the url used for executing the webhook (returned by the webhooks OAuth2
        flow)

    :param guild_id:
        the guild id this webhook is for, if any
    """

    id: Snowflake
    type: WebhookType

    channel_id: Optional[Snowflake] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    application_id: Optional[Snowflake] = None

    user: APINullable[User] = MISSING
    token: APINullable[str] = MISSING
    source_guild: APINullable[Guild] = MISSING
    source_channel: APINullable[Channel] = MISSING
    url: APINullable[str] = MISSING

    guild_id: APINullable[Optional[Snowflake]] = MISSING
