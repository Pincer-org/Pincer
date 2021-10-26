# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from sys import modules
from typing import TypeVar, Callable, Coroutine, Any, Union, Literal, Tuple

from pincer.exceptions import InvalidAnnotation


class MissingType:
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
            raise InvalidAnnotation(
                "Descripted arguments must be a tuple of length 2. "
                "(if you are using this as the intented type, just "
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
