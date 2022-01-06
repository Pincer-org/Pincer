# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, fields, _is_dataclass_instance
from enum import Enum, EnumMeta
from inspect import getfullargspec
from typing import (
    Dict, Tuple, Union, Generic, TypeVar, Any, TYPE_CHECKING,
    List, get_type_hints, get_origin, get_args
)

from .conversion import construct_client_dict
from .types import MissingType, MISSING, TypeCache
from ..exceptions import InvalidArgumentAnnotation

if TYPE_CHECKING:
    from ..objects.guild.channel import Channel
    from ..objects.guild.guild import Guild
    from ..client import Client

T = TypeVar("T")

_log = logging.getLogger(__package__)


def _asdict_ignore_none(obj: Generic[T]) -> Union[Tuple, Dict, T]:
    """
    Returns a dict from a dataclass that ignores
    all values that are None
    Modification of _asdict_inner from dataclasses

    Parameters
    ----------

    obj: Generic[T]
        The object to convert

    Returns
    -------
        A dict without None values
    """

    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            value = _asdict_ignore_none(getattr(obj, f.name))

            if isinstance(value, Enum):
                result.append((f.name, value.value))
            # This if statement was added to the function
            elif not isinstance(value, MissingType) and not f.name.startswith("_"):
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
        # Iterates through the meta items, these are keys whom should
        # be added to every object. But to keep typehints we have to
        # define those in the parent class. Yet this gives a conflict
        # because the value is not defined. (that's why we remove it)
        for key in HTTPMeta.__meta_items:
            if mapping.get("__annotations__") and \
                    (value := mapping["__annotations__"].get(key)):
                # We want to keep the type annotations of the objects
                # tho, so lets statically store them, so we can read
                # them later.
                HTTPMeta.__ori_annotations.update({key: value})
                del mapping["__annotations__"][key]

        # Instantiate our object
        http_object = super().__new__(mcs, name, base, mapping)

        # Read all removed items
        if getattr(http_object, "__annotations__", None):
            for k, v in HTTPMeta.__ori_annotations.items():
                http_object.__annotations__[k] = v
                setattr(http_object, k, None)

        return http_object


@dataclass(repr=False)
class APIObject(metaclass=HTTPMeta):
    """
    Represents an object which has been fetched from the Discord API.
    """
    _client: Client

    def __get_types(self, attr: str, arg_type: type) -> Tuple[type]:
        """Get the types from type annotations.

        Parameters
        ----------
        attr: :class:`str`
            The attribute the typehint belongs to.
        arg_type: :class:`type`
            The type annotation for the attribute.

        Returns
        -------
        Tuple[:class:`type`]
            A collection of type annotation(s). Will most of the time
            consist of 1 item.

        Raises
        ------
        :class:`~pincer.exceptions.InvalidArgumentAnnotation`
            Exception which is raised when the type annotation has not enough
            or too many arguments for the parser to handle.
        """
        origin = get_origin(arg_type)

        if origin is Union:
            # Ahh yes, typing module has no type annotations for this...
            # noinspection PyTypeChecker
            args: Tuple[type] = get_args(arg_type)

            if 2 <= len(args) < 4:
                return args

            raise InvalidArgumentAnnotation(
                f"Attribute `{attr}` in `{type(self).__name__}` has too many "
                f"or not enough arguments! (got {len(args)} expected 2-3)"
            )

        return arg_type,

    def __attr_convert(self, attr_value: Dict, attr_type: T) -> T:
        """Convert an attribute to the requested attribute type using
        the factory or the __init__.

        Parameters
        ----------
        attr: :class:`str`
            The attribute the typehint belongs to.
        arg_type: T
            The type annotation for the attribute.

        Returns
        -------
        T
            The instantiated version of the arg_type.
        """
        factory = attr_type

        # Always use `__factory__` over __init__
        if getattr(attr_type, "__factory__", None):
            factory = attr_type.__factory__

        if attr_value is MISSING:
            return MISSING

        if attr_type is not None and isinstance(attr_value, attr_type):
            return attr_value

        if isinstance(attr_value, dict):
            return factory(construct_client_dict(self._client, attr_value))

        return factory(attr_value)

    def __post_init__(self):
        self._http = getattr(self._client, "http", None)
        TypeCache()

        # Get all type annotations for the attributes.
        attributes = get_type_hints(self, globalns=TypeCache.cache).items()

        for attr, attr_type in attributes:
            # Ignore private attributes.
            if attr.startswith('_'):
                continue

            types = self.__get_types(attr, attr_type)

            types = tuple(filter(
                lambda tpe: tpe is not None and tpe is not MISSING,
                types
            ))

            if not types:
                raise InvalidArgumentAnnotation(
                    f"Attribute `{attr}` in `{type(self).__name__}` only "
                    "consisted of missing/optional type!"
                )

            specific_tp = types[0]

            attr_gotten = getattr(self, attr)

            if tp := get_origin(specific_tp):
                specific_tp = tp

            if isinstance(specific_tp, EnumMeta) and not attr_gotten:
                attr_value = MISSING
            elif tp == list and attr_gotten and (classes := get_args(types[0])):
                attr_value = [
                    self.__attr_convert(attr_item, classes[0])
                    for attr_item in attr_gotten
                ]
            elif tp == dict and attr_gotten and (classes := get_args(types[0])):
                attr_value = {
                    key: self.__attr_convert(value, classes[1])
                    for key, value in attr_gotten.items()
                }
            else:
                attr_value = self.__attr_convert(attr_gotten, specific_tp)

            setattr(self, attr, attr_value)

    # Set default factory method to from_dict for APIObject's.
    @classmethod
    def __factory__(cls: Generic[T], *args, **kwargs) -> T:
        return cls.from_dict(*args, **kwargs)

    def __repr__(self):
        attrs = ', '.join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
            if v and not k.startswith('_')
        )

        return f"{type(self).__name__}({attrs})"

    def __str__(self):
        # TODO: fix docs
        """

        Returns
        -------

        """
        if _name := getattr(self, "__name__", None):
            return f"{_name} {self.__class__.__name__.lower()}"

        return super().__str__()

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
        Transform the current object to a dictionary representation. Parameters that
        start with an underscore are not serialized.
        """
        return _asdict_ignore_none(self)


class GuildProperty:

    @property
    def guild(self) -> Guild:
        """Return a guild from an APIObject
        Parameters
        ----------
        self : :class:`~pincer.utils.api_object.APIObject`

        Returns
        -------
        :class:`~pincer.objects.guild.guild.Guild`
        """
        return self._client.guilds[self.guild_id]


class ChannelProperty:

    @property
    def channel(self) -> Channel:
        """Return a channel from an APIObject
        Parameters
        ----------
        obj : :class:`~pincer.utils.api_object.APIObject`

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
        """
        return self._client.channels[self.channel_id]
