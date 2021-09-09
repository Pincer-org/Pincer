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

from __future__ import annotations

import copy
from dataclasses import dataclass, fields, _is_dataclass_instance
from enum import Enum
from typing import Dict, Union, Generic, TypeVar

from .types import MissingType

T = TypeVar("T")


def _asdict_ignore_none(obj: Generic[T]) -> Union[tuple, dict, T]:
    """
    Returns a dict from a dataclass that ignores
    all values that are None
    Modification of _asdict_inner from dataclasses

    :param obj:
        Dataclass obj
    """

    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_ignore_none(getattr(obj, f.name))

            if isinstance(value, Enum):
                result.append((f.name, value.value))
            # This if statement was added to the function
            elif not isinstance(value, MissingType):
                result.append((f.name, value))

        return dict(result)

    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_asdict_ignore_none(v) for v in obj])

    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_ignore_none(v) for v in obj)

    elif isinstance(obj, dict):
        return type(obj)(
            (
                _asdict_ignore_none(k),
                _asdict_ignore_none(v)
            ) for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


@dataclass
class APIObject:
    """
    Represents an object which has been fetched from the Discord API.
    """

    # def __post_init__(self):
    #     fin = {
    #         key: _eval_type(ForwardRef(value), globals(), globals())
    #         for key, value in self.__annotations__.items()
    #     }
    #
    #     # pprint(self.__annotations__)
    #     # pprint(get_type_hints(self))
    #     print(fin)
    #     print("Post init", self)

    @classmethod
    def from_dict(cls: Generic[T], data: Dict[str, Union[str, bool, int]]) -> T:
        """
        Parse an API object from a dictionary.
        """
        if isinstance(data, cls):
            return data

        # Disable inspection for IDE because this is valid code for the
        # inherited classes:
        # noinspection PyArgumentList
        return cls(**{
            key: (value.value if isinstance(value, Enum)
                  else value) for key, value in data.items()
        })

    def to_dict(self) -> Dict:
        """
        Transform the current object to a dictionary representation.
        """
        return _asdict_ignore_none(self)
