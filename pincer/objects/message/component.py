# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ..app.select_menu import SelectOption
    from ..message.button import ButtonStyle
    from ..message.emoji import Emoji
    from ...utils import APINullable


@dataclass
class MessageComponent(APIObject):
    """
    Represents a Discord Message Component object

    :param type:
        component type

    :param custom_id:
        a developer-defined identifier for the component,
        max 100 characters

    :param disabled:
        whether the component is disabled,
        defaults to `False`

    :param style:
        one of button styles

    :param label:
        text that appears on the button, max 80 characters

    :param emoji:
        `name`, `id`, and `animated`

    :param url:
        a url for link-style buttons

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

    :param components:
        a list of child components
    """
    type: int
    options: List[SelectOption]

    custom_id: APINullable[str] = MISSING
    disabled: APINullable[bool] = False
    style: APINullable[ButtonStyle] = MISSING
    label: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    url: APINullable[str] = MISSING
    placeholder: APINullable[str] = MISSING
    min_values: APINullable[int] = 1
    max_values: APINullable[int] = 1
    components: APINullable[List[MessageComponent]] = MISSING
