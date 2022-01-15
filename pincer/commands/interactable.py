# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:
    from typing import Any


_log = logging.getLogger(__name__)

T = TypeVar("T")


class PartialInteractable(ABC):
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.func.__call__(*args, **kwds)

    @abstractmethod
    def register(self, manager: Any) -> type[T]:
        """Registers a command to a command handler to be called later"""


class Interactable:
    def __init__(self) -> None:
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, PartialInteractable):
                setattr(self, key, value.register(self))
