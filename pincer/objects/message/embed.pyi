from ...exceptions import EmbedFieldError as EmbedFieldError, InvalidUrlError as InvalidUrlError
from ...utils.api_object import APIObject as APIObject
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, Optional, Union

class EmbedAuthor:
    icon_url: APINullable[str]
    name: APINullable[str]
    proxy_icon_url: APINullable[str]
    url: APINullable[str]
    def __post_init__(self) -> None: ...

class EmbedImage:
    url: APINullable[str]
    proxy_url: APINullable[str]
    height: APINullable[int]
    width: APINullable[int]
    def __post_init__(self) -> None: ...

class EmbedProvider:
    name: APINullable[str]
    url: APINullable[str]

class EmbedThumbnail:
    url: APINullable[str]
    proxy_url: APINullable[str]
    height: APINullable[int]
    width: APINullable[int]
    def __post_init__(self) -> None: ...

class EmbedVideo:
    height: APINullable[int]
    url: APINullable[str]
    proxy_url: APINullable[str]
    width: APINullable[int]

class EmbedFooter:
    text: str
    icon_url: APINullable[str]
    proxy_icon_url: APINullable[str]
    def __post_init__(self) -> None: ...

class EmbedField:
    name: str
    value: str
    inline: APINullable[bool]
    def __post_init__(self) -> None: ...

class Embed(APIObject):
    title: APINullable[str]
    description: APINullable[str]
    color: APINullable[int]
    fields: list[EmbedField]
    footer: APINullable[EmbedFooter]
    image: APINullable[EmbedImage]
    provider: APINullable[EmbedProvider]
    thumbnail: APINullable[EmbedThumbnail]
    timestamp: APINullable[str]
    author: APINullable[EmbedAuthor]
    url: APINullable[str]
    video: APINullable[EmbedVideo]
    type: APINullable[int]
    def __post_init__(self) -> None: ...
    def set_timestamp(self, time: datetime) -> Embed: ...
    def set_author(self, icon_url: APINullable[str] = ..., name: APINullable[str] = ..., proxy_icon_url: APINullable[str] = ..., url: APINullable[str] = ...) -> Embed: ...
    def set_image(self, url: APINullable[str] = ..., proxy_url: APINullable[str] = ..., height: APINullable[int] = ..., width: APINullable[int] = ...) -> Embed: ...
    def set_thumbnail(self, height: APINullable[int] = ..., url: APINullable[str] = ..., proxy_url: APINullable[str] = ..., width: APINullable[int] = ...) -> Embed: ...
    def set_footer(self, text: str, icon_url: APINullable[str] = ..., proxy_icon_url: APINullable[str] = ...) -> Embed: ...
    def add_field(self, name: str, value: str, inline: APINullable[bool] = ...) -> Embed: ...
    def add_fields(self, field_list: Union[Dict[Any, Any], Iterable[Iterable[Any, Any]]], checks: Optional[Callable[[Any], Any]] = ..., map_title: Optional[Callable[[Any], str]] = ..., map_values: Optional[Callable[[Any], str]] = ..., inline: bool = ...) -> Embed: ...
