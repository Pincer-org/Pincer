from ...utils.api_object import APIObject as APIObject
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..message.emoji import Emoji as Emoji
from enum import IntEnum

class ButtonStyle(IntEnum):
    PRIMARY: int
    SECONDARY: int
    SUCCESS: int
    DANGER: int
    LINK: int

class Button(APIObject):
    type: int
    style: ButtonStyle
    label: APINullable[str]
    emoji: APINullable[Emoji]
    custom_id: APINullable[str]
    url: APINullable[str]
    disabled: APINullable[bool]
