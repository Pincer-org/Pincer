# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import copy
from dataclasses import dataclass, fields, _is_dataclass_instance
from enum import Enum
from inspect import getfullargspec
from typing import Dict, Tuple, Union, Generic, TypeVar, Any, TYPE_CHECKING, \
    Optional, List

from .types import MissingType

if TYPE_CHECKING:
    from ..client import Client
    from ..core.http import HTTPClient

T = TypeVar("T")


def _asdict_ignore_none(obj: Generic[T]) -> Union[Tuple, Dict, T]:
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


class HTTPMeta(type):
    __meta_items: List[str] = ["_client", "_http"]
    __ori_annotations: Dict[str, type] = {}

    def __new__(mcs, name, base, mapping):
        for key in HTTPMeta.__meta_items:
            if mapping.get("__annotations__") and \
                    (value := mapping["__annotations__"].get(key)):
                HTTPMeta.__ori_annotations.update({key: value})
                del mapping["__annotations__"][key]

        http_object = super().__new__(mcs, name, base, mapping)

        if getattr(http_object, "__annotations__", None):
            for k, v in HTTPMeta.__ori_annotations.items():
                http_object.__annotations__[k] = v
                setattr(http_object, k, None)

        return http_object


@dataclass
class APIObject(metaclass=HTTPMeta):
    """
    Represents an object which has been fetched from the Discord API.
    """
    _client: Client
    _http: HTTPClient

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
    def from_dict(
            cls: Generic[T],
            data: Dict[str, Union[str, bool, int, Any]]
    ) -> T:
        """
        Parse an API object from a dictionary.
        """
        if isinstance(data, cls):
            return data

        # Disable inspection for IDE because this is valid code for the
        # inherited classes:
        # noinspection PyArgumentList
        return cls(**dict(map(
            lambda key: (
                key,
                data[key].value if isinstance(data[key], Enum) else data[key]
            ),
            filter(
                lambda object_argument: data.get(object_argument) is not None,
                getfullargspec(cls.__init__).args
            )
        )))

    def to_dict(self) -> Dict:
        """
        Transform the current object to a dictionary representation.
        """
        return _asdict_ignore_none(self)
