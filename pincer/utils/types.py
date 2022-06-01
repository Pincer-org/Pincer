# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from sys import modules
from typing import TypeVar, Callable, Coroutine, Any, Union, Optional


class MissingType:
    """Type class for missing attributes and parameters."""

    def __repr__(self):
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False

    def __eq__(self, __o: object) -> bool:
        return __o is MISSING

    def __hash__(self) -> int:
        # By returning the hash of None, when searching for a command it doesn't know
        # what kind of "nothing" it is.
        return hash(None)


MISSING = MissingType()


T = TypeVar("T")

JSONSerializable = TypeVar(
    "JSONSerializable", str, int, float, list, dict, bool, None
)


# Represents a value which is optionally returned from the API
APINullable = Union[T, MissingType]


#: Represents a coroutine.
Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])

choice_value_types = Union[str, int, float]

CheckFunction = Optional[Callable[[Any], bool]]


class Singleton(type):
    # Thanks to this stackoverflow answer (method 3):
    # https://stackoverflow.com/q/6760685/12668716
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
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
