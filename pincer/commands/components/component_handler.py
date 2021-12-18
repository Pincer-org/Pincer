# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Callable, Dict

from ...utils.types import Singleton


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
