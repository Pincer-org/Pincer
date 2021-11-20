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


class Color:
    """
    A color in RGB.

    Parameters
    ---------
    c : Union[:class:`str`,:class:`int`]
        The hex color in the format ``#NNNNNN`` or an int with the RGB values.
    Attributes
    r : :class:`int`
        The red value for this color.
    g : :class:`int`
        The green value for this color.
    b : :class:`int`
        The blue value for this color.
    """
    def __init__(self, c: Union[str, int]) -> None:
        if isinstance(c, int):
            self.r = c >> 16 & 255
            self.g = c >> 8 & 255
            self.b = c & 255
            return

        # Conversion modified from this answer
        # https://stackoverflow.com/a/29643643
        self.r, self.g, self.b = (int(c[n + 1:n + 3], 16) for n in (0, 2, 4))

    @property
    def rbg(self):
        """
        Returns
        -------
        Tuple[:class:`int`, :class:`int` :class:`int`]
            Tuple value for rgb.
        """
        return self.r, self.g, self.b

    @property
    def hex(self):
        """
        Returns
        str
            Str value for hex.
        """
        return f"{hex(self.r)[2:]}{hex(self.g)[2:]}{hex(self.b)[2:]}"
