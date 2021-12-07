# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Callable, Dict

from ..utils.types import Singleton


def hash_button_id(_id):
    return str(hash(id))


# I'm ignoring the name collision so `button(id="str")` is valid code
def button(func=None, id=None, hash_id=True):

    def wrap(id):
        id = hash_button_id(id)
        ButtonHandler().register_id(id, func)
        return func

    if func is None:
        return wrap

    return wrap(id)


class ButtonHandler(metaclass=Singleton):

    def __init__(self) -> None:
        self.buttons: Dict[str, Callable] = {}

    def register_id(self, _id: str, func: Callable):
        self.buttons[_id] = func

    def __getitem__(self, _id):
        return self.buttons[_id]
