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
from typing import Dict, Union

from websockets.typing import Data

from pincer.utils.constants import MissingType


def _asdict_ignore_none(
        obj: APIObject,
        dict_factory
) -> Union[tuple, dict, APIObject]:
    """
    Returns a dict from a dataclass that ignores
    all values that are None
    Modification of _asdict_inner from dataclasses

    :param obj: Dataclass obj
    :param dict_factory: Dict
    """

    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_ignore_none(getattr(obj, f.name), dict_factory)
            
            # This if statement was added to the function
            if not isinstance(value, MissingType):
                result.append((f.name, value))

        return dict_factory(result)

    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_asdict_ignore_none(v, dict_factory) for v in obj])

    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_ignore_none(v, dict_factory) for v in obj)

    elif isinstance(obj, dict):
        return type(obj)(
            (
                _asdict_ignore_none(k, dict_factory),
                _asdict_ignore_none(v, dict_factory)
            ) for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


@dataclass
class APIObject:

    @classmethod
    def from_dict(cls, data: Data[str, Union[str, bool, int]]) -> APIObject:
        # TODO: Write documentation
        return cls(**data)

    def to_dict(self) -> Dict:
        return _asdict_ignore_none(self, dict)
