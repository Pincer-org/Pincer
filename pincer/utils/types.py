# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from sys import modules
from typing import (
    TYPE_CHECKING, TypeVar, Callable, Coroutine, Any, Union, Literal, Optional
)

from pincer.exceptions import InvalidArgumentAnnotation

if TYPE_CHECKING:
    from typing import Tuple


class MissingType:
    """Type class for missing attributes and parameters."""

    def __repr__(self):
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False


MISSING = MissingType()


T = TypeVar('T')


# Represents a value which is optionally returned from the API
APINullable = Union[T, MissingType]


# Represents a coroutine.
Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


Choices = Literal


choice_value_types = (str, int, float)

CheckFunction = Optional[Callable[[Any], bool]]


class Singleton(type):
    # Thanks to this stackoverflow answer (method 3):
    # https://stackoverflow.com/q/6760685/12668716
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton,
                cls
            ).__call__(*args, **kwargs)
        return cls._instances[cls]


class TypeCache(metaclass=Singleton):
    cache = {}

    def __init__(self):
        # Register all known types to the cache. This gets used later
        # to auto-convert the properties to their desired type.
        lcp = modules.copy()
        for module in lcp:
            if not module.startswith("pincer"):
                continue

            TypeCache.cache.update(lcp[module].__dict__)


class _TypeInstanceMeta(type):
    def __getitem__(cls, args: Tuple[T, str]):
        if not isinstance(args, tuple) or len(args) != 2:
            raise InvalidArgumentAnnotation(
                "Descripted arguments must be a tuple of length 2. "
                "(if you are using this as the indented type, just "
                "pass two arguments)"
            )

        return cls(*args)


class Descripted(metaclass=_TypeInstanceMeta):
    # TODO: Write example & more docs
    """Description type."""

    def __init__(self, key: Any, description: str):
        if not isinstance(description, str):
            raise RuntimeError(
                "The description value must always be a string!"
            )

        self.key = key
        self.description = description
