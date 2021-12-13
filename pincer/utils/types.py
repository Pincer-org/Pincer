# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from __future__ import annotations

from sys import modules
from typing import (
    TypeVar, Callable, Coroutine, Any, Union, Optional, Dict, List
)


class MissingType:
    """Type class for missing attributes and parameters."""

    def __repr__(self):
        return "<MISSING>"

    def __getitem__(self, item):
        return self

    def __getattr__(self, item):
        return self

    def __bool__(self) -> bool:
        return False


MISSING = MissingType()


T = TypeVar("T")

JsonVal = Optional[Union[str, int, float, bool, Dict[str, Any], List[Any]]]
JsonDict = Dict[str, JsonVal]

# Represents a value which is optionally returned from the API
APINullable = Union[T, MissingType]


#: Represents a coroutine.
Coro = Callable[[Any, Any], Coroutine[Any, Any, Any]]

choice_value_types = Union[str, int, float]

CheckFunction = Optional[Callable[[Any], bool]]


class Singleton(type):
    # Thanks to this stackoverflow answer (method 3):
    # https://stackoverflow.com/q/6760685/12668716
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton,
                cls
            ).__call__(*args, **kwargs)
        return cls._instances[cls]


class TypeCache(metaclass=Singleton):
    cache: Dict[Any, Any] = {}

    def __init__(self):
        # Register all known types to the cache. This gets used later
        # to auto-convert the properties to their desired type.
        lcp = modules.copy()
        for module in lcp:
            if not module.startswith("pincer"):
                continue

            TypeCache.cache.update(lcp[module].__dict__)
