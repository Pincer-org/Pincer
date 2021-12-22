from ...utils.api_object import APIObject as APIObject
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from ..app.select_menu import SelectOption as SelectOption
from ..message.button import ButtonStyle as ButtonStyle
from ..message.emoji import Emoji as Emoji
from typing import List

class MessageComponent(APIObject):
    type: int
    options: List[SelectOption]
    custom_id: APINullable[str]
    disabled: APINullable[bool]
    style: APINullable[ButtonStyle]
    label: APINullable[str]
    emoji: APINullable[Emoji]
    url: APINullable[str]
    placeholder: APINullable[str]
    min_values: APINullable[int]
    max_values: APINullable[int]
    components: APINullable[List[MessageComponent]]
