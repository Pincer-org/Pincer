# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from dataclasses import dataclass

from ...utils.types import MISSING
from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Dict

    from ..user.user import User
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


class CallbackType(IntEnum):
    """The types of response a client can give to a interaction.
    """
    PONG = 1 #: ACK a Ping
    MESSAGE = 4 #: Respond to an interaction with a message
    DEFERRED_MESSAGE = 5 #: ACK an interaction and edit a response later, the user sees a loading state
    DEFERRED_UPDATE_MESSAGE = 6 #: For components, ACK an interaction and edit the original message later; the user does not see a loading state
    UPDATE_MESSAGE = 7 #: For components, edit the message the component was attached to


class InteractionType(IntEnum):
    """Represents the different types of interactions the client
    can have with a member.
    """
    PING = 1 #: Ping an interaction
    APPLICATION_COMMAND = 2 #: A "slash" command
    MESSAGE_COMPONENT = 3 #: A ui compoment like buttons and selects


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
    member: :class:`~pincer.utios.types.APINullable`\\[Dict]
        The member who invoked the interaction
    """
    id: Snowflake
    type: InteractionType
    name: str
    user: User

    member: APINullable[Dict] = MISSING
