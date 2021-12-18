# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from functools import partial
from typing import Callable, Dict, List

from ..objects.message.emoji import Emoji
from ..utils.conversion import remove_none
from ..utils.types import MISSING, Singleton

from .button import Button, ButtonStyle
from .select_menu import SelectMenu, SelectOption


def component(custom_id):
    def wrap(custom_id, func):
        ComponentHandler().register_id(_id=custom_id, func=func)
        return func

    return partial(wrap, custom_id)


def button(
    label: str,
    style: ButtonStyle,
    emoji: Emoji = None,
    url: str = None,
    disabled: bool = None,
    custom_id: str = None
):

    def wrap(custom_id, func):

        if custom_id is None:
            custom_id = func.__name__

        ComponentHandler().register_id(custom_id, func)

        button = Button(
            # Hack to not override defaults in button class
            **remove_none(
                {
                    "custom_id": custom_id,
                    "style": style,
                    "label": label,
                    "disabled": disabled,
                    "emoji": emoji,
                    "url": url
                }
            )
        )

        button.func = func
        button.__call__ = partial(func)

        return button

    return partial(wrap, custom_id)


def select_menu(
    options: List[SelectOption] = None,
    placeholder: str = None,
    min_values: int = None,
    max_values: int = None,
    disabled: bool = None,
    custom_id: str = None
):

    def wrap(custom_id, func):

        if custom_id is None:
            custom_id = func.__name__

        ComponentHandler().register_id(custom_id, func)

        menu = SelectMenu(
            # Hack to not override defaults in button class
            **remove_none(
                {
                    "custom_id": custom_id,
                    "options": options,
                    "placeholder": placeholder,
                    "min_values": min_values,
                    "max_values": max_values,
                    "disabled": disabled
                }
            )
        )

        menu.func = func
        menu.__call__ = partial(func)

        return menu

    return partial(wrap, custom_id)


class ComponentHandler(metaclass=Singleton):
    """Handles registered components

    Attributes
    ----------
    register : Dict[:class:`str`, :class:`Callable`]
        Dictionary of registered buttons.
    """

    register: Dict[str, Callable] = {}

    def register_id(self, _id: str, func: Callable):
        self.register[_id] = func
