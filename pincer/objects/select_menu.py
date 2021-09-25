# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import List

from .emoji import Emoji
from ..utils import APIObject, APINullable, MISSING


@dataclass
class SelectOption(APIObject):
    """
    Represents a Discord Select Option object

    :param label:
        the user-facing name of the option, max 100 characters

    :param value:
        the def-defined value of the option, max 100 characters

    :param description:
        an additional description of the option, max 100 characters

    :param emoji:
        `id`, `name`, and `animated`

    :param default:
        will render this option as selected by default
    """
    label: str
    value: str
    description: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    default: APINullable[bool] = MISSING


@dataclass
class SelectMenu(APIObject):
    """
    Represents a Discord Select Menu object

    :param type:
        `3` for a select menu

    :param custom_id:
        a developer-defined identifier for the button,
        max 100 characters

    :param options:
        the choices in the select, max 25

    :param placeholder:
        custom placeholder text if nothing is selected,
        max 100 characters

    :param min_values:
        the minimum number of items that must be chosen;
        default 1, min 0, max 25

    :param max_values:
        the maximum number of items that can be chosen;
         default 1, max 25

    :param disabled:
        disable the select, default False
    """
    type: int
    custom_id: str
    options: List[SelectOption]

    placeholder: APINullable[str] = MISSING
    min_values: APINullable[int] = 1
    max_values: APINullable[int] = 1
    disabled: APINullable[bool] = False
