# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Callable

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils.types import APINullable
    from ...objects.message.emoji import Emoji


class ButtonStyle(IntEnum):
    """Buttons come in a variety of styles to convey different types of actions.
    These styles also define what fields are valid for a button.

    Attributes
    ----------
    Primary:
        - color: blurple
        - required_field: custom_id
    Secondary:
        - color: gray
        - required_field: custom_id
    Success:
        - color: green
        - required_field: custom_id
    Danger:
        - color: red
        - required_field: custom_id
    Link:
        - color: gray, navigates to a URL
        - required_field: url
    """
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


@dataclass(repr=False)
class Button(APIObject):
    """Represents a Discord Button object.
    Buttons are interactive components that render on messages.

    They can be clicked by users,
    and send an interaction to your app when clicked.

    Attributes
    ----------
    style: :class:`~pincer.objects.message.button.ButtonStyle`
        one of button styles
    label: APINullable[:class:`str`]
        text that appears on the button, max 80 characters
    emoji: APINullable[:class:`~pincer.objects.message.emoji.Emoji`]
        ``name``, ``id``, and ``animated``
    custom_id: APINullable[:class:`str`]
        A developer-defined identifier for the button,
        max 100 characters
    url: APINullable[:class:`str`]
        A url for link-style buttons
    disabled: APINullable[:class:`bool`]
        Whether the button is disabled (default `False`)
    """
    custom_id: APINullable[str]
    label: APINullable[str]
    style: ButtonStyle

    emoji: APINullable[Emoji] = MISSING
    url: APINullable[str] = MISSING
    disabled: APINullable[bool] = False

    type: int = 2
    _func: Callable = None

    def __post_init__(self):
        self.type = 2

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
