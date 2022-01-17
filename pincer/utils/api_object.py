# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import copy
import logging
from dataclasses import fields, _is_dataclass_instance
from enum import Enum, EnumMeta
from inspect import getfullargspec
from itertools import chain
from typing import (
    Dict,
    Tuple,
    Union,
    Generic,
    TypeVar,
    Any,
    TYPE_CHECKING,
    get_type_hints,
    get_origin,
    get_args,
    Optional,
)

from .types import MissingType, MISSING, TypeCache
from ..exceptions import InvalidArgumentAnnotation

if TYPE_CHECKING:
    from ..core import HTTPClient
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
            elif not isinstance(value, MissingType) and not f.name.startswith(
                "_"
            ):
                result.append((f.name, value))

        return dict(result)

    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[_asdict_ignore_none(v) for v in obj])

    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_ignore_none(v) for v in obj)

    elif isinstance(obj, dict):
        return type(obj)(
            (_asdict_ignore_none(k), _asdict_ignore_none(v))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


class APIObject:
    """
    Represents an object which has been fetched from the Discord API.
    """

    _client: Optional[Client] = None

    @property
    def _http(self) -> HTTPClient:
        if not self._client:
            raise AttributeError("Object is not yet linked to a client")

        return self._client.http

    @classmethod
    def bind_client(cls, client: Client):
        """
        Links the object to the client.

        Parameters
        ----------
        client: Client
            The client to link to.
        """
        cls._client = client

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

        return (arg_type,)

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
            return factory(attr_value)

        return factory(attr_value)

    def __post_init__(self):
        TypeCache()

        attributes = chain.from_iterable(
            get_type_hints(cls, globalns=TypeCache.cache).items()
            for cls in chain(self.__class__.__bases__, (self,))
        )

        for attr, attr_type in attributes:
            # Ignore private attributes.
            if attr.startswith("_"):
                continue

            types = self.__get_types(attr, attr_type)

            types = tuple(
                filter(
                    lambda tpe: tpe is not None and tpe is not MISSING, types
                )
            )

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
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if v and not k.startswith("_")
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
        cls: Generic[T], data: Dict[str, Union[str, bool, int, Any]]
    ) -> T:
        """
        Parse an API object from a dictionary.
        """
        if isinstance(data, cls):
            return data

        # Disable inspection for IDE because this is valid code for the
        # inherited classes:
        # noinspection PyArgumentList
        return cls(
            **dict(
                map(
                    lambda key: (
                        key,
                        data[key].value
                        if isinstance(data[key], Enum)
                        else data[key],
                    ),
                    filter(
                        lambda object_argument: data.get(object_argument)
                        is not None,
                        getfullargspec(cls.__init__).args,
                    ),
                )
            )
        )

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
