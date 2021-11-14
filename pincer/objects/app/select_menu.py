# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List

    from ..message.emoji import Emoji
    from ...utils.types import APINullable


@dataclass
class SelectOption(APIObject):
    """Represents a Discord Select Option object

    Attributes
    ----------
    label: :class:`str`
        The user-facing name of the option, max 100 characters
    value: :class:`str`
        The def-defined value of the option, max 100 characters
    description: APINullable[:class:`str`]
        An additional description of the option, max 100 characters
    emoji: APINullable[:class:`~pincer.objects.message.emoji.Emoji`]
        ``id``, ``name``, and ``animated``
    default: APINullable[:class:`bool`]
        Will render this option as selected by default
    """
    label: str
    value: str
    description: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    default: APINullable[bool] = MISSING


@dataclass
class SelectMenu(APIObject):
    """Represents a Discord Select Menu object

    Attributes
    ----------
    type: :class:`int`
        ``3`` for a select menu
    custom_id: :class:`str`
        A developer-defined identifier for the button,
        max 100 characters
    options: List[:class:`~pincer.objects.app.select_menu.SelectOption`]
        The choices in the select, max ``25``
    placeholder: APINullable[:class:`str`]
        Custom placeholder text if nothing is selected,
        max 100 characters
    min_values: APINullable[:class:`int`]
        The minimum number of items that must be chosen; min ``0``, max ``25``
        |default| ``1``
    max_values: APINullable[:class:`int`]
        The maximum number of items that can be chosen; max 25
        |default| ``1``
    disabled: APINullable[:class:`bool`]
        Disable the select
        |default| False
    """
    type: int
    custom_id: str
    options: List[SelectOption]

    placeholder: APINullable[str] = MISSING
    min_values: APINullable[int] = 1
    max_values: APINullable[int] = 1
    disabled: APINullable[bool] = False
