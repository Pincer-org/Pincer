# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List

    from ..app.select_menu import SelectOption
    from ..message.button import ButtonStyle
    from ..message.emoji import Emoji
    from ...utils.types import APINullable


@dataclass
class MessageComponent(APIObject):
    """Represents a Discord Message Component object

    Attributes
    ----------
    type: :class:`int`
        Component type
    options: List[:class:`~pincer.objects.app.select_menu.SelectOption`]
        The choices in the select, max 25
    custom_id: APINullable[:class:`str`]
        A developer-defined identifier for the component,
        max 100 characters
    disabled: APINullable[:class:`bool`]
        Whether the component is disabled,
        defaults to `False`
    style: APINullable[:class:`~pincer.objects.message.button.ButtonStyle`]
        One of button styles
    label: APINullable[:class:`str`]
        Text that appears on the button, max 80 characters
    emoji: APINullable[:class:`~pincer.objects.message.emoji.Emoji`]
        ``name``, ``id``, and ``animated``
    url: APINullable[:class:`str`]
        A url for link-style buttons
    placeholder: APINullable[:class:`str`]
        Custom placeholder text if nothing is selected,
        max 100 characters
    min_values: APINullable[:class:`int`]
        The minimum number of items that must be chosen;
        |default| ``1``, min ``0``, max ``25``
    max_values: APINullable[:class:`int`]
        The maximum number of items that can be chosen;
        |default| ``1``, max ``25``
    components: APINullable[List[:class:`~pincer.objects.message.component.MessageComponent`]]
        A list of child components
    """
    # noqa: E501
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
