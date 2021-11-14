# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Any, Optional, Protocol, TypeVar

T = TypeVar("T")


class GetItem(Protocol):
    """Represents a class which implements the __getitem__ property."""
    def __getitem__(self, key: int) -> Any:
        return ...


def get_index(
        collection: GetItem,
        index: int,
        fallback: Optional[T] = None
) -> Optional[T]:
    """Gets an item from a collection through index.
    Allows you to provide a fallback for if that index is out of bounds.

    Parameters
    ----------
    collection: :class:`~pincer.utils.extraction.GetItem`
        The collection from which the item is retrieved.
    index: :class:`int`
        The index of the item in the collection.
    fallback: Optional[T]
        The fallback value which will be used if the index doesn't
        exist. Default value is None.

    Returns
    -------
    Optional[T]
        The item at the provided index from the collection, or if that
        item doesn't exist it will return the fallback value.
    """

    try:
        return collection[index]

    except IndexError:
        return fallback
