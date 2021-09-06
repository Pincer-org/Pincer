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
from enum import Enum
from typing import Dict

from pincer.objects.application_command import \
    ApplicationCommandInteractionDataOption
from pincer.objects.channel import Channel
from pincer.objects.member import Member
from pincer.objects.role import Role
from pincer.objects.select_menu import SelectOption
from pincer.objects.user import User
from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, APINullable
from pincer.utils.snowflake import Snowflake


class InteractionType(Enum):
    """
    Represents the different types of interactions the client
    can have with a member.

    :param CHAT_INPUT:
        Slash commands; a text-based command that shows up when a user types /

    :param USER:
        A UI-based command that shows up when you right click or tap on a user

    :param MESSAGE:
        A UI-based command that shows up when you right click or tap on a message
    """
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 2


@dataclass
class ResolvedData(APIObject):
    """
    Represents a Discord Resolved Data structure

    :param users:
        Map of Snowflakes to user objects

    :param members:
        Map of Snowflakes to partial member objects

    :param roles:
        Map of Snowflakes to role objects

    :param channels:
        Map of Snowflakes to partial channel objects

    :param messages:
        Map of Snowflakes to partial message objects
    """
    users: APINullable[Dict[Snowflake, User]] = MISSING
    members: APINullable[Dict[Snowflake, Member]] = MISSING
    roles: APINullable[Dict[Snowflake, Role]] = MISSING
    channels: APINullable[Dict[Snowflake, Channel]] = MISSING
    messages: APINullable[Dict[Snowflake, ...]] = MISSING
    # Message


@dataclass
class InteractionData(APIObject):
    """
    Represents a Discord Interaction Data structure

    :param id:
        the `ID` of the invoked command

    :param name:
        the `name` of the invoked command

    :param type:
        the `type` of the invoked command

    :param resolved:
        converted users + roles + channels

    :param options:
        the params + values from the user

    :param custom_id:
        the `custom_id` of the component

    :param component_type:
        the type of the component

    :param values:
        the values the user selected

    :param target_id:
        id of the user or message targeted by a user or message command
    """
    id: Snowflake
    name: str
    type: int

    resolved: APINullable[ResolvedData] = MISSING
    options: APINullable[ApplicationCommandInteractionDataOption] = MISSING
    custom_id: APINullable[str] = MISSING
    component_type: APINullable[int] = MISSING
    values = APINullable[SelectOption] = MISSING
    target_id = APINullable[Snowflake] = MISSING


@dataclass
class MessageInteraction(APIObject):
    """
    Represents a Discord Message Interaction object

    This is sent on the message object when the message
    is a response to an Interaction without an existing message.

    :param id: id of the interaction
    :param type: the type of interaction
    :param name: the name of the application command
    :param user: the user who invoked the interaction
    """
    id: Snowflake
    type: InteractionType
    name: str
    user: User


@dataclass
class Interaction(APIObject):
    """
    Represents a Discord Interaction object

    :param id:
        id of the interaction

    :param application_id:
        id of the application this interaction is for

    :param type:
        the type of interaction

    :param data:
        the command data payload

    :param guild_id:
        the guild it was sent from

    :param channel_id:
        the channel it was sent from

    :param member:
        guild member data for the invoking user, including permissions

    :param user:
        user object for the invoking user, if invoked in a DM

    :param token:
        a continuation token for responding to the interaction

    :param version:
        read-only property, always `1`

    :param message:
        for components, the message they were attached to
    """
    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    token: str

    version: int = 1
    data: APINullable[InteractionData] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    channel_id: APINullable[Snowflake] = MISSING
    member: APINullable[Member] = MISSING
    user: APINullable[User] = MISSING
    message: APINullable[...] = MISSING  # Message
