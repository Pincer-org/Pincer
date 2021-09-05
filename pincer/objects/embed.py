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

from dataclasses import dataclass, field
from datetime import datetime

from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, OptionallyProvided


class EmbedFieldError(ValueError):
    """Exception that is raised when an embed field is too large"""

    @classmethod
    def from_desc(cls, _type: str, max_size: int, cur_size: int):
        return cls(
            f"{_type} can have a maximum length of {max_size}."
            f" (Current size: {cur_size})"
        )


class InvalidUrlError(ValueError):
    pass


def _field_size(f: str) -> int:
    """
    The Discord API removes white space when counting the length of a field

    :param f: The field.
    :return: Length of the string without white space.
    """
    return 0 if f == MISSING else len(f.strip())


def _is_valid_url(url: str) -> bool:
    return (
        url.startswith("http://")
        or url.startswith("https://")
        or url.startswith("attachment://")
    )


@dataclass
class EmbedAuthor:
    """
    Representation of the Embed Author class

    :param name: Name of the author
    :param url: Url of the author
    :param icon_url: Url of the author icon
    :param proxy_icon_url: A proxied url of the author icon
    """
    icon_url: OptionallyProvided[str] = MISSING
    name: OptionallyProvided[str] = MISSING
    proxy_icon_url: OptionallyProvided[str] = MISSING
    url: OptionallyProvided[str] = MISSING

    def __post_init__(self):
        if _field_size(self.name) > 256:
            raise EmbedFieldError.from_desc("Author name", 256, len(self.name))

        if not _is_valid_url(self.url):
            raise InvalidUrlError("Url must be http, https, or attachment.")


@dataclass
class EmbedImage:
    """
    Representation of the Embed Image class

    :param url: Source url of the image
    :param proxy_url: A proxied url of the image
    :param height: Height of the image
    :param width: Width of the image
    """

    height: OptionallyProvided[int] = MISSING
    proxy_url: OptionallyProvided[str] = MISSING
    url: OptionallyProvided[str] = MISSING
    width: OptionallyProvided[int] = MISSING

    def __post_init__(self):
        if not _is_valid_url(self.url):
            raise InvalidUrlError("Url must be http, https, or attachment.")


@dataclass
class EmbedProvider:
    """
    Representation of the Provider class

    :param name: Name of the provider
    :param url: Url of the provider
    """
    name: OptionallyProvided[str] = MISSING
    url: OptionallyProvided[str] = MISSING


@dataclass
class EmbedThumbnail:
    """
    Representation of the Embed Thumbnail class

    :param url: Source url of the thumbnail
    :param proxy_url: A proxied url of the thumbnail
    :param height: Height of the thumbnail
    :param width: Width of the thumbnail
    """

    height: OptionallyProvided[int] = MISSING
    proxy_url: OptionallyProvided[str] = MISSING
    url: OptionallyProvided[str] = MISSING
    width: OptionallyProvided[int] = MISSING

    def __post_init__(self):
        if not _is_valid_url(self.url):
            raise InvalidUrlError("Url must be http, https, or attachment.")


@dataclass
class EmbedVideo:
    """
    Representation of the Embed Video class

    :param url: Source url of the video
    :param proxy_url: A proxied url of the video
    :param height: Height of the video
    :param width: Width of the video
    """
    height: OptionallyProvided[int] = MISSING
    url: OptionallyProvided[str] = MISSING
    proxy_url: OptionallyProvided[str] = MISSING
    width: OptionallyProvided[int] = MISSING


@dataclass
class EmbedFooter:
    """
    Representation of the Embed Footer class

    :param text: Footer text
    :param icon_url: Url of the footer icon
    :param proxy_icon_url: A proxied url of the footer icon
    """

    text: str

    icon_url: OptionallyProvided[str] = MISSING
    proxy_icon_url: OptionallyProvided[str] = MISSING

    def __post_init__(self):
        if _field_size(self.text) > 2048:
            raise EmbedFieldError.from_desc(
                "Footer text", 2048, len(self.text)
            )


@dataclass
class EmbedField:
    """
    Representation of the Embed Field class

    :param name: The name of the field
    :param value: The text in the field
    :param inline: Whether or not this field should display inline
    """

    name: str
    value: str

    inline: OptionallyProvided[bool] = MISSING

    def __post_init__(self):
        if _field_size(self.name) > 256:
            raise EmbedFieldError.from_desc(
                "Field name", 256, len(self.name)
            )

        if _field_size(self.value) > 1024:
            raise EmbedFieldError.from_desc(
                "Field value", 1024, len(self.value)
            )


# TODO: Handle Bad Request if embed that is too big is sent
# https://discord.com/developers/docs/resources/channel#embed-limits
# Currently ignored since I don't think it would make sense to put
# This with the Embed class
@dataclass
class Embed(APIObject):
    """
    Representation of the discord Embed class

    :param author: Author information.
    :param color: Embed color code.
    :param description: Embed description.
    :param fields: Fields information.
    :param footer: Footer information.
    :param image: Image information.
    :param provider: Provider information.
    :param thumbnail: Thumbnail information.
    :param timestamp: Timestamp of embed content in ISO format.
    :param title: Embed title.
    :param url: Embed url.
    :param video: Video information.
    """

    author: OptionallyProvided[EmbedAuthor] = MISSING
    color: OptionallyProvided[int] = MISSING
    description: OptionallyProvided[str] = MISSING
    fields: list[EmbedField] = field(default_factory=list)
    footer: OptionallyProvided[EmbedFooter] = MISSING
    image: OptionallyProvided[EmbedImage] = MISSING
    provider: OptionallyProvided[EmbedProvider] = MISSING
    thumbnail: OptionallyProvided[EmbedThumbnail] = MISSING
    timestamp: OptionallyProvided[str] = MISSING
    title: OptionallyProvided[str] = MISSING
    url: OptionallyProvided[str] = MISSING
    video: OptionallyProvided[EmbedVideo] = MISSING

    def __post_init__(self):
        if _field_size(self.title) > 256:
            raise EmbedFieldError.from_desc(
                "Embed title", 256, len(self.title)
            )

        if _field_size(self.description) > 4096:
            raise EmbedFieldError.from_desc(
                "Embed description", 4096, len(self.description)
            )

        if len(self.fields) > 25:
            raise EmbedFieldError.from_desc(
                "Embed field", 25, len(self.fields)
            )

    def set_timestamp(self, time: datetime):
        """
        Discord uses iso format for time stamps.
        This function will set the time to that format.
        :param time: A datetime object.
        """
        self.timestamp = time.isoformat()

    def set_author(
        self,
        icon_url: OptionallyProvided[str] = MISSING,
        name: OptionallyProvided[str] = MISSING,
        proxy_icon_url: OptionallyProvided[str] = MISSING,
        url: OptionallyProvided[str] = MISSING
    ) -> Embed:

        self.author = EmbedAuthor(
            icon_url=icon_url,
            name=name,
            proxy_icon_url=proxy_icon_url,
            url=url
        )

        return self

    def set_image(
        self,
        height: OptionallyProvided[int] = MISSING,
        url: OptionallyProvided[str] = MISSING,
        proxy_url: OptionallyProvided[str] = MISSING,
        width: OptionallyProvided[int] = MISSING
    ) -> Embed:
        """
        :param url: Source url of the video
        :param proxy_url: A proxied url of the video
        :param height: Height of the video
        :param width: Width of the video
        """
        self.video = EmbedImage(
            height=height,
            url=url,
            proxy_url=proxy_url,
            width=width
        )

    def set_provider(
        self,
        name: OptionallyProvided[str] = MISSING,
        url: OptionallyProvided[str] = MISSING
    ) -> Embed:
        """
        :param name: Name of the provider
        :param url: Url of the provider
        """
        self.provider = EmbedProvider(name=name, url=url)
        return self

    def set_thumbnail(
        self,
        height: OptionallyProvided[int] = MISSING,
        url: OptionallyProvided[str] = MISSING,
        proxy_url: OptionallyProvided[str] = MISSING,
        width: OptionallyProvided[int] = MISSING
    ) -> Embed:
        """
        :param url: Source url of the video
        :param proxy_url: A proxied url of the video
        :param height: Height of the video
        :param width: Width of the video
        """
        self.video = EmbedThumbnail(
            height=height,
            url=url,
            proxy_url=proxy_url,
            width=width
        )

        return self

    def set_video(
        self,
        height: OptionallyProvided[int] = MISSING,
        url: OptionallyProvided[str] = MISSING,
        proxy_url: OptionallyProvided[str] = MISSING,
        width: OptionallyProvided[int] = MISSING
    ) -> Embed:
        """
        :param url: Source url of the video
        :param proxy_url: A proxied url of the video
        :param height: Height of the video
        :param width: Width of the video
        """
        self.video = EmbedVideo(
            height=height,
            url=url,
            proxy_url=proxy_url,
            width=width
        )

        return self

    def set_footer(
        self,
        text: str,
        icon_url: OptionallyProvided[str] = MISSING,
        proxy_icon_url: OptionallyProvided[str] = MISSING
    ) -> Embed:
        """
        :param text: Footer text
        :param icon_url: Url of the footer icon
        :param proxy_icon_url: A proxied url of the footer icon
        """
        self.footer = EmbedFooter(
            text=text,
            icon_url=icon_url,
            proxy_icon_url=proxy_icon_url
        )

        return self

    def add_field(
        self,
        name: str,
        value: str,
        inline: OptionallyProvided[bool] = MISSING
    ) -> Embed:
        """
        :param name: The name of the field
        :param value: The text in the field
        :param inline: Whether or not this field should display inline
        """
        _field = EmbedField(
            name=name,
            value=value,
            inline=inline
        )

        if len(self.fields) > 25:
            raise EmbedFieldError.from_desc(
                "Embed field", 25, len(self.fields)+1
            )

        self.fields += [_field]

        return self
