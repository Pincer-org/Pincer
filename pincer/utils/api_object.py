# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, fields, _is_dataclass_instance
from enum import Enum, EnumMeta
from inspect import getfullargspec
from sys import modules
from typing import (
    Dict, Tuple, Union, Generic, TypeVar, Any, TYPE_CHECKING,
    List, get_type_hints, get_origin, get_args
)

from .conversion import convert
from .types import MissingType, Singleton, MISSING
from ..exceptions import InvalidAnnotation

if TYPE_CHECKING:
    from ..client import Client
    from ..core.http import HTTPClient

T = TypeVar("T")

_log = logging.getLogger(__package__)


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


class TypeCache(metaclass=Singleton):
    cache = {}

    def __init__(self):
        lcp = modules.copy()
        for module in lcp:
            if not module.startswith("pincer"):
                continue

            TypeCache.cache.update(lcp[module].__dict__)


@dataclass
class APIObject(metaclass=HTTPMeta):
    """
    Represents an object which has been fetched from the Discord API.
    """
    _client: Client
    _http: HTTPClient

    def __get_types(self, attr: str, arg_type: type) -> Tuple[Any]:
        origin = get_origin(arg_type)

        if origin is Union:
            args = get_args(arg_type)

            if 2 <= len(args) < 4:
                return args

            raise InvalidAnnotation(
                f"Attribute `{attr}` in `{type(self).__name__}` has too many "
                f"or not enough arguments! (got {len(args)} expected 2-3)"
            )

        return arg_type,

    def __attr_convert(self, attr: str, attr_type: T) -> T:
        factory = attr_type

        if getattr(attr_type, "__factory__", None):
            factory = attr_type.__factory__

        return convert(
            getattr(self, attr),
            factory,
            attr_type,
            self._client
        )

    def __post_init__(self):
        TypeCache()

        attributes = get_type_hints(self, globalns=TypeCache.cache).items()

        for attr, attr_type in attributes:
            if attr.startswith('_'):
                continue

            types = self.__get_types(attr, attr_type)

            types = tuple(filter(
                lambda tpe: tpe is not None and tpe is not MISSING,
                types
            ))

            if not types:
                raise InvalidAnnotation(
                    f"Attribute `{attr}` in `{type(self).__name__}` only "
                    "consisted of missing/optional type!"
                )

            specific_tp = types[0]

            if tp := get_origin(specific_tp):
                specific_tp = tp

            if isinstance(specific_tp, EnumMeta) and not getattr(self, attr):
                attr_value = MISSING
            else:
                attr_value = self.__attr_convert(attr, specific_tp)

            setattr(self, attr, attr_value)

    @classmethod
    def __factory__(cls: Generic[T], *args, **kwargs) -> T:
        return cls.from_dict(*args, **kwargs)

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
