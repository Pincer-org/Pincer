# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import TypeVar, Callable, Coroutine, Any, Union


class MissingType:
    def __repr__(self):
        return "<MISSING>"


MISSING = MissingType()

T = TypeVar('T')

# Represents a value which is optionally returned from the API
APINullable = Union[T, MissingType]

# Represents a coroutine.
Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])
