# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ._component import _Component
from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List

    from ...objects.message.emoji import Emoji
    from ...utils.types import APINullable


@dataclass(repr=False)
class SelectOption(APIObject):
    """Represents a Discord Select Option

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
    value: APINullable[str] = MISSING
    description: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    default: APINullable[bool] = MISSING

    def __post_init__(self):
        super().__post_init__()

        if self.value is MISSING:
            self.value = self.label


@dataclass(repr=False)
class SelectMenu(_Component):
    """Represents a Discord Select Menu

    Attributes
    ----------
    custom_id: :class:`str`
        A developer-defined identifier for the button,
        max 100 characters
    options: List[:class:`~pincer.commands.components.select_menu.SelectOption`]
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
        Disable the selects
        |default| False
    """

    custom_id: str
    options: Optional[List[SelectOption]] = None

    placeholder: APINullable[str] = MISSING
    min_values: APINullable[int] = 1
    max_values: APINullable[int] = 1
    disabled: APINullable[bool] = False

    type: int = 3

    def __post_init__(self):
        self.type = 3

    def with_options(self, *options: SelectOption) -> SelectMenu:
        """
        Sets the ``options`` parameter to \\*options and returns a new
        :class:`~pincer.commands.components.select_menu.SelectMenu`.

        \\*options : SelectOption
            List of options to set
        """
        copied_obj = copy(self)
        copied_obj.options = options
        return copied_obj

    def with_appended_options(self, *options: SelectOption) -> SelectMenu:
        """
        Append \\*options to the ``options`` parameter and returns a new
        :class:`~pincer.commands.components.select_menu.SelectMenu`.

        \\*options : SelectOption
            List of options to append
        """
        copied_obj = copy(self)
        copied_obj.options += options
        return copied_obj
