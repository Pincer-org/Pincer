# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Any, Optional, Protocol, TypeVar

T = TypeVar("T")


class GetItem(Protocol):
    def __getitem__(self, key: int) -> Any:
        return ...


def get_index(
        collection: GetItem,
        index: int,
        fallback: Optional[T] = None
) -> Optional[T]:
    try:
        return collection[index]

    except IndexError:
        return fallback
