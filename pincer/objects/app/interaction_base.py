# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Dict

    from ..user.user import User
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


class CallbackType(IntEnum):
    """The types of response a client can give to a interaction.

    Attributes
    ----------
    PONG:
        ACK a Ping
    MESSAGE:
        Respond to an interaction with a message
    DEFERRED_MESSAGE:
        ACK an interaction and edit a response later, the user sees a loading
        state
    DEFERRED_UPDATE_MESSAGE:
        For components, ACK an interaction and edit the original message later
    UPDATE_MESSAGE:
        For components, edit the message the component was attached to
    """
    # noqa: E501
    PONG = 1
    MESSAGE = 4
    DEFERRED_MESSAGE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7


class InteractionType(IntEnum):
    """Represents the different types of interactions the client
    can have with a member.

    Attributes
    ----------
    PING:
        Ping an interaction.
    APPLICATION_COMMAND:
        A "slash" command.
    MESSAGE_COMPONENT:
        A ui component like buttons and selects.
    """
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3


@dataclass
class MessageInteraction(APIObject):
    """Represents a Discord Message Interaction object

    This is sent on the message object when the message
    is a response to an Interaction without an existing message.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the interaction
    type: :class:`~pincer.objects.app.interaction_base.InteractionType`
        The type of interaction
    name: :class:`str`
        The name of the application command
    user: :class:`~pincer.objects.user.user.User`
        The user who invoked the interaction
    member: APINullable[Dict]
        The member who invoked the interaction
    """
    id: Snowflake
    type: InteractionType
    name: str
    user: User

    member: APINullable[Dict] = MISSING
