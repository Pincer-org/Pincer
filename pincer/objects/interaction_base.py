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
from enum import IntEnum

from .user import User
from ..utils import APIObject, Snowflake


class CallbackType(IntEnum):
    """
    The types of response a client can give to a interaction.

    :param PONG:
        ACK a Ping

    :param MESSAGE:
        respond to an interaction with a message

    :param DEFERRED_MESSAGE:
            ACK an interaction and edit a response later, the user sees a loading state

    :param DEFERRED_UPDATE_MESSAGE:
        for components, ACK an interaction and edit the original message later; the user does not see a loading state

    :param UPDATE_MESSAGE
        for components, edit the message the component was attached to
    """
    PONG = 1
    MESSAGE = 4
    DEFERRED_MESSAGE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7


class InteractionType(IntEnum):
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
    MESSAGE_COMPONENT = 3


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
