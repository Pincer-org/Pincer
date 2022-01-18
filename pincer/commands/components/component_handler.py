# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Dict


from ._component import _Component
from ...utils.types import Singleton
from ...objects.app.command import InteractableStructure


class ComponentHandler(metaclass=Singleton):
    """Handles registered components

    Attributes
    ----------
    register : Dict[:class:`str`, :class:`Callable`]
        Dictionary of registered buttons.
    """

    register: Dict[str, InteractableStructure[_Component]] = {}
