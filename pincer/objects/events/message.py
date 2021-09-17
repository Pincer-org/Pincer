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

from pincer.objects.emoji import Emoji
from pincer.objects.guild_member import GuildMember
from pincer.utils.api_object import APIObject
from pincer.utils.snowflake import Snowflake
from pincer.utils.types import APINullable, MISSING


@dataclass
class MessageDeleteEvent(APIObject):
    """
    Sent when a message is deleted.

    :param id:
        the id of the message

    :param channel_id:
        the id of the channel

    :param guild_id:
        the id of the guild
    """
    id: Snowflake
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageDeleteBulkEvent(APIObject):
    """
    Sent when multiple messages are deleted at once.

    :param ids:
        the ids of the messages

    :param channel_id:
        the id of the channel

    :param guild_id:
        the id of the guild
    """
    ids: List[Snowflake]
    channel_id: Snowflake

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionAddEvent(APIObject):
    """
    Sent when a user adds a reaction to a message.

    :param user_id:
        the id of the user

    :param channel_id:
        the id of the channel

    :param message_id:
        the id of the message

    :param guild_id:
        the id of the guild

    :param member:
        the member who reacted if this happened in a guild

    :param emoji:
        the emoji used to react
    """
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING


@dataclass
class MessageReactionRemoveEvent(APIObject):
    """
    Sent when a user removes a reaction from a message.

    :param user_id:
        the id of the user

    :param channel_id:
        the id of the channel

    :param message_id:
        the id of the message

    :param guild_id:
        the id of the guild

    :param emoji:
        the emoji used to react
    """
    user_id: Snowflake
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionRemoveAllEvent(APIObject):
    """
    Sent when a user explicitly removes all reactions from a message.

    :param channel_id:
        the id of the channel

    :param message_id:
        the id of the message

    :param guild_id:
        the id of the guild
    """
    channel_id: Snowflake
    message_id: Snowflake
    guild_id: APINullable[Snowflake] = MISSING


@dataclass
class MessageReactionRemoveEmojiEvent(APIObject):
    """
    Sent when a bot removes all instances of a given
    emoji from the reactions of a message.

    :param channel_id:
        the id of the channel

    :param guild_id:
        the id of the guild

    :param message_id:
        the id of the message

    :param emoji:
        the emoji that was removed
    """
    channel_id: Snowflake
    message_id: Snowflake
    emoji: Emoji

    guild_id: APINullable[Snowflake] = MISSING
