# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from functools import partial
from typing import List

from .component_handler import ComponentHandler
from ...objects.message.emoji import Emoji
from ...utils.conversion import remove_none

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
) -> Button:

    def wrap(custom_id, func) -> Button:

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
                    "url": url,
                    "_func": func
                }
            )
        )

        button.func = func
        button.__call__ = partial(func)

        return button

    return partial(wrap, custom_id)


def select_menu(
    func=None,
    options: List[SelectOption] = None,
    placeholder: str = None,
    min_values: int = None,
    max_values: int = None,
    disabled: bool = None,
    custom_id: str = None
) -> SelectMenu:

    def wrap(custom_id, func) -> SelectMenu:

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
                    "disabled": disabled,
                    "_func": func
                }
            )
        )

        return menu

    if func is None:
        return partial(wrap, custom_id)

    return wrap(custom_id, func)
