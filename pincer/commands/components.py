# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Callable, Dict

from ..utils.types import Singleton


def hash_component_id(_id):
    return str(hash(id))


# I'm ignoring the name collision so `component(id="str")` is valid code
def component(func=None, id=None, hash_id=True):

    def wrap(func, id=None):
        id = hash_component_id(id)
        ComponentHandler().register_id(id, func)
        return func

    if func is None:
        return wrap

    return wrap(func, id)


class ComponentHandler(metaclass=Singleton):
    """Handles registered components
    
    
    """

    register: Dict[str, Callable] = {}

    def register_id(self, _id: str, func: Callable):
        self.register[_id] = func
