from ...utils.api_object import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..user.user import User as User
from enum import IntEnum
from typing import Dict

class CallbackType(IntEnum):
    PONG: int
    MESSAGE: int
    DEFERRED_MESSAGE: int
    DEFERRED_UPDATE_MESSAGE: int
    UPDATE_MESSAGE: int

class InteractionType(IntEnum):
    PING: int
    APPLICATION_COMMAND: int
    MESSAGE_COMPONENT: int

class MessageInteraction(APIObject):
    id: Snowflake
    type: InteractionType
    name: str
    user: User
    member: APINullable[Dict]
