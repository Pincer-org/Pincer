# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from typing import Any, Optional, Protocol, TypeVar

T = TypeVar("T")


class GetItem(Protocol):
    """
    Represents a class which implements the __getitem__ property.
    """

    def __getitem__(self, key: int) -> Any:
        ...


def get_index(
        collection: GetItem,
        index: int,
        fallback: Optional[T] = None
) -> Optional[T]:
    """
    Gets an item from a collection through index. Allows you to provide
    a fallback for if that index is out of bounds.

    :param collection:
        The collection from which the item is retrieved.

    :param index:
        The index of the item in the collection.

    :param fallback:
        The fallback value which will be used if the index doesn't
        exist. Default value is None.

    :return:
        The item at the provided index from the collection, or if that
        item doesn't exist it will return the fallback value.
    """
    try:
        return collection[index]

    except IndexError:
        return fallback
