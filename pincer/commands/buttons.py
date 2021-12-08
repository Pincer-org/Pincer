# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Callable, Dict

from ..utils.types import Singleton


def hash_button_id(_id):
    return str(hash(id))


# I'm ignoring the name collision so `button(id="str")` is valid code
def button(func=None, id=None, hash_id=True):

    def wrap(func, id=None):
        id = hash_button_id(id)
        ButtonHandler().register_id(id, func)
        return func

    if func is None:
        return wrap

    return wrap(func, id)


class ButtonHandler(metaclass=Singleton):

    register: Dict[str, Callable] = {}

    def register_id(self, _id: str, func: Callable):
        self.register[_id] = func
