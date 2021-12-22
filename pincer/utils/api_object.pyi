from ..client import Client as Client
from ..exceptions import InvalidArgumentAnnotation as InvalidArgumentAnnotation
from ..objects.guild.channel import Channel as Channel
from ..objects.guild.guild import Guild as Guild
from .types import MISSING as MISSING, MissingType as MissingType, TypeCache as TypeCache
from pincer.utils.conversion import construct_client_dict as construct_client_dict
from typing import Any, Dict, TypeVar, Union

T = TypeVar('T')

class HTTPMeta(type):
    def __new__(mcs, name, base, mapping): ...

class APIObject(metaclass=HTTPMeta):
    def __post_init__(self): ...
    @classmethod
    def __factory__(cls, *args, **kwargs) -> T: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, bool, int, Any]]) -> T: ...
    def to_dict(self) -> Dict: ...

class GuildProperty:
    @property
    def guild(self) -> Guild: ...

class ChannelProperty:
    @property
    def channel(self) -> Channel: ...
