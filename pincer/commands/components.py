# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from functools import partial
from typing import Callable, Dict

from ..utils.types import Singleton


def hash_component_id(_id):
    return str(hash(_id))


def component(custom_id, hash_id=True):

    def wrap(custom_id, hash_id, func):
        if hash_id:
            custom_id = hash_component_id(custom_id)
        ComponentHandler().register_id(_id=custom_id, func=func)
        return func

    return partial(wrap, custom_id, hash_id)


class ComponentHandler(metaclass=Singleton):
    """Handles registered components
    
    
    """

    register: Dict[str, Callable] = {}

    def register_id(self, _id: str, func: Callable):
        self.register[_id] = func
