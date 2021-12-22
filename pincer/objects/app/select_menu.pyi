from ...utils.api_object import APIObject as APIObject
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..message.emoji import Emoji as Emoji
from typing import List

class SelectOption(APIObject):
    label: str
    value: str
    description: APINullable[str]
    emoji: APINullable[Emoji]
    default: APINullable[bool]

class SelectMenu(APIObject):
    type: int
    custom_id: str
    options: List[SelectOption]
    placeholder: APINullable[str]
    min_values: APINullable[int]
    max_values: APINullable[int]
    disabled: APINullable[bool]
