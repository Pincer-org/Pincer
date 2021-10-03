# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ..message.emoji import Emoji
    from ...utils import APINullable


class ButtonStyle(IntEnum):
    """
    Buttons come in a variety of styles to convey different types of actions.
    These styles also define what fields are valid for a button.

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


@dataclass
class Button(APIObject):
    """
    Represents a Discord Button object.
    Buttons are interactive components that render on messages.

    They can be clicked by users,
    and send an interaction to your app when clicked.

    :param type:
        `2` for a button

    :param style:
        one of button styles

    :param label:
        text that appears on the button, max 80 characters

    :param emoji:
        `name`, `id`, and `animated`

    :param custom_id:
        a developer-defined identifier for the button,
        max 100 characters

    :param url:
        a url for link-style buttons

    :param disabled:
        whether the button is disabled (default `False`)
    """
    type: int
    style: ButtonStyle

    label: APINullable[str] = MISSING
    emoji: APINullable[Emoji] = MISSING
    custom_id: APINullable[str] = MISSING
    url: APINullable[str] = MISSING
    disabled: APINullable[bool] = False
