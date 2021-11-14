# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from re import match
from typing import TYPE_CHECKING

from ...exceptions import InvalidUrlError, EmbedFieldError
from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Iterable, Union, Optional

    from ...utils.types import APINullable


def _field_size(_field: str) -> int:
    """
    The Discord API removes white space
        when counting the length of a field.

    :param _field:
        The field.

    :return:
        Length of the string without white space.
    """
    return 0 if _field == MISSING else len(_field.strip())


def _is_valid_url(url: str) -> bool:
    """
    Checks whether the url is a proper and valid url.
    (matches for http and attachment protocol.

    :param url:
        The url which must be checked.

    :return:
        Whether the provided url is valid.
    """
    stmt = (
        r"(http[s]|attachment)"
        r"?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
        r"(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )

    return bool(match(stmt, url))


def _check_if_valid_url(url: str):
    """Checks if the provided url is valid.

    Raises
    ------
    :class:`~pincer.exceptions.InvalidUrlError`
        if the url didn't match the url regex.
        (which means that it was malformed or didn't match the http/attachment
        protocol).
    """
    if not _is_valid_url(url):
        raise InvalidUrlError(
            "Url was malformed or wasn't of protocol http(s)/attachment."
        )


@dataclass
class EmbedAuthor:
    """Representation of the Embed Author class

    Attributes
    ----------
    name: APINullable[:class:`str`]
        Name of the author
    url: APINullable[:class:`str`]
        Url of the author
    icon_url: APINullable[:class:`str`]
        Url of the author icon
    proxy_icon_url: APINullable[:class:`str`]
        A proxied url of the author icon
    """
    icon_url: APINullable[str] = MISSING
    name: APINullable[str] = MISSING
    proxy_icon_url: APINullable[str] = MISSING
    url: APINullable[str] = MISSING

    def __post_init__(self):  # stop documenting special methods
        if _field_size(self.name) > 256:
            raise EmbedFieldError.from_desc("Author name", 256, len(self.name))

        _check_if_valid_url(self.url)


@dataclass
class EmbedImage:
    """Representation of the Embed Image class

    Attributes
    ----------
    url: APINullable[:class:`str`]
        Source url of the image
    proxy_url: APINullable[:class:`str`]
        A proxied url of the image
    height: APINullable[:class:`int`]
        Height of the image
    width: APINullable[:class:`int`]
        Width of the image
    """

    url: APINullable[str] = MISSING
    proxy_url: APINullable[str] = MISSING
    height: APINullable[int] = MISSING
    width: APINullable[int] = MISSING

    def __post_init__(self):
        _check_if_valid_url(self.url)


@dataclass
class EmbedProvider:
    """Representation of the Provider class

    Attributes
    ----------
    name: APINullable[:class:`str`]
        Name of the provider
    url: APINullable[:class:`str`]
        Url of the provider
    """
    name: APINullable[str] = MISSING
    url: APINullable[str] = MISSING


@dataclass
class EmbedThumbnail:
    """Representation of the Embed Thumbnail class

    Attributes
    ----------
    url: APINullable[:class:`str`]
        Source url of the thumbnail
    proxy_url: APINullable[:class:`str`]
        A proxied url of the thumbnail
    height: APINullable[:class:`int`]
        Height of the thumbnail
    width: APINullable[:class:`int`]
        Width of the thumbnail
    """

    url: APINullable[str] = MISSING
    proxy_url: APINullable[str] = MISSING
    height: APINullable[int] = MISSING
    width: APINullable[int] = MISSING

    def __post_init__(self):
        _check_if_valid_url(self.url)


@dataclass
class EmbedVideo:
    """Representation of the Embed Video class

    Attributes
    ----------
    url: APINullable[:class:`str`]
        Source url of the video
    proxy_url: APINullable[:class:`str`]
        A proxied url of the video
    height: APINullable[:class:`int`]
        Height of the video
    width: APINullable[:class:`int`]
        Width of the video
    """
    height: APINullable[int] = MISSING
    url: APINullable[str] = MISSING
    proxy_url: APINullable[str] = MISSING
    width: APINullable[int] = MISSING


@dataclass
class EmbedFooter:
    """Representation of the Embed Footer class

    Attributes
    ----------
    text: :class:`str`
        Footer text
    icon_url: APINullable[:class:`str`]
        Url of the footer icon
    proxy_icon_url: APINullable[:class:`str`]
        A proxied url of the footer icon

    Raises
    ------
    EmbedFieldError:
        Text is longer than 2048 characters
    """

    text: str

    icon_url: APINullable[str] = MISSING
    proxy_icon_url: APINullable[str] = MISSING

    def __post_init__(self):
        if _field_size(self.text) > 2048:
            raise EmbedFieldError.from_desc(
                "Footer text", 2048, len(self.text)
            )


@dataclass
class EmbedField:
    """Representation of the Embed Field class

    Attributes
    ----------
    name: :class:`str`
        The name of the field
    value: :class:`str`
        The text in the field
    inline: APINullable[:class:`bool`]
        Whether or not this field should display inline

    Raises
    ------
    EmbedFieldError:
        Name is longer than 256 characters
    EmbedFieldError:
        Description is longer than 1024 characters
    """

    name: str
    value: str

    inline: APINullable[bool] = MISSING

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
    """Representation of the discord Embed class

    Attributes
    ----------
    title: APINullable[:class:`str`]
        Embed title.
    description: APINullable[:class:`str`]
        Embed description.
    color: APINullable[:class:`int`]
        Embed color code.
    fields: List[:class:`~pincer.objects.message.embed.EmbedField`]
        Fields information.
    footer: APINullable[:class:`~pincer.objects.message.embed.EmbedFooter`]
        Footer information.
    image: APINullable[:class:`~pincer.objects.message.embed.EmbedImage`]
        Image information.
    provider: APINullable[:class:`~pincer.objects.message.embed.EmbedProvider`]
        Provider information.
    thumbnail: APINullable[:class:`~pincer.objects.message.embed.EmbedThumbnail`]
        Thumbnail information.
    timestamp: APINullable[:class:`str`]
        Timestamp of embed content in ISO format.
    url: APINullable[:class:`str`]
        Embed url.
    video: APINullable[:class:`~pincer.objects.message.embed.EmbedVideo`]
        Video information.
    type: APINullable[:class:`int`]
        type of message
    """
    # noqa: E501

    title: APINullable[str] = MISSING
    description: APINullable[str] = MISSING
    color: APINullable[int] = MISSING
    fields: list[EmbedField] = field(default_factory=list)
    footer: APINullable[EmbedFooter] = MISSING
    image: APINullable[EmbedImage] = MISSING
    provider: APINullable[EmbedProvider] = MISSING
    thumbnail: APINullable[EmbedThumbnail] = MISSING
    timestamp: APINullable[str] = MISSING
    author: APINullable[EmbedAuthor] = MISSING
    url: APINullable[str] = MISSING
    video: APINullable[EmbedVideo] = MISSING
    type: APINullable[int] = MISSING

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

    def set_timestamp(self, time: datetime) -> Embed:
        """Discord uses iso format for time stamps.
        This function will set the time to that format.

        Parameters
        ----------
        time : :class:`datetime.datetime`
            The datetime to set the timestamp to.

        Returns
        -------
        :class:`~pincer.objects.message.embed.Embed`
            The new embed object.
        """
        self.timestamp = time.isoformat()

        return self

    def set_author(
            self,
            icon_url: APINullable[str] = MISSING,
            name: APINullable[str] = MISSING,
            proxy_icon_url: APINullable[str] = MISSING,
            url: APINullable[str] = MISSING
    ) -> Embed:
        """Set the author message for the embed. This is the top
        field of the embed.

        Parameters
        ----------
        icon_url: APINullable[:class:`str`]
            The icon which will be next to the author name.
        name: APINullable[:class:`str`]
            The name for the author (so the message).
        proxy_icon_url: APINullable[:class:`str`]
            A proxied url of the author icon.
        url: APINullable[:class:`str`]
            The url for the author name, this will make the
            name field a link/url.

        Returns
        -------
        :class:`~pincer.objects.message.embed.Embed`
            The new embed object.
        """

        self.author = EmbedAuthor(
            icon_url=icon_url,
            name=name,
            proxy_icon_url=proxy_icon_url,
            url=url
        )

        return self

    def set_image(
            self,
            url: APINullable[str] = MISSING,
            proxy_url: APINullable[str] = MISSING,
            height: APINullable[int] = MISSING,
            width: APINullable[int] = MISSING
    ) -> Embed:
        """Sets an image for your embed.

        Parameters
        ----------
        url: APINullable[:class:`str`]
            Source url of the video
        proxy_url: APINullable[:class:`str`]
            A proxied url of the video
        height: APINullable[:class:`int`]
            Height of the video
        width: APINullable[:class:`int`]
            Width of the video

        Returns
        -------
        :class:`~pincer.objects.message.embed.Embed`
            The new embed object.
        """
        self.image = EmbedImage(
            height=height,
            url=url,
            proxy_url=proxy_url,
            width=width
        )

        return self

    def set_thumbnail(
            self,
            height: APINullable[int] = MISSING,
            url: APINullable[str] = MISSING,
            proxy_url: APINullable[str] = MISSING,
            width: APINullable[int] = MISSING
    ) -> Embed:  # ? its normally smaller in the corner?
        """Sets the thumbnail of the embed.
        This image is bigger than the ``image`` property.

        url: APINullable[:class:`str`]
            Source url of the video
        proxy_url: APINullable[:class:`str`]
            A proxied url of the video
        height: APINullable[:class:`int`]
            Height of the video
        width: APINullable[:class:`int`]
            Width of the video

        Returns
        -------
        :class:`~pincer.objects.message.embed.Embed`
            The new embed object.
        """
        self.thumbnail = EmbedThumbnail(
            height=height,
            url=url,
            proxy_url=proxy_url,
            width=width
        )

        return self

    def set_footer(
            self,
            text: str,
            icon_url: APINullable[str] = MISSING,
            proxy_icon_url: APINullable[str] = MISSING
    ) -> Embed:
        """
        Sets the embed footer. This is at the bottom of your embed.

        Parameters
        ----------
        text: :class:`str`
            Footer text
        icon_url: APINullable[:class:`str`]
            Url of the footer icon
        proxy_icon_url: APINullable[:class:`str`]
            A proxied url of the footer icon

        Returns
        -------
        :class:`~pincer.objects.message.embed.Embed`
            The new embed object.
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
            inline: APINullable[bool] = MISSING
    ) -> Embed:
        """Adds a field to the embed.
        An embed can contain up to 25 fields.

        Parameters
        ----------
        name: :class:`str`
            The name of the field
        value: :class:`str`
            The text in the field
        inline: APINullable[:class:`bool`]
            Whether or not this field should display inline

        Raises
        ------
        EmbedFieldError:
            Raised when there are more than 25 fields in the embed
        """
        _field = EmbedField(
            name=name,
            value=value,
            inline=inline
        )

        if len(self.fields) > 25:
            raise EmbedFieldError.from_desc(
                "Embed field", 25, len(self.fields) + 1
            )

        self.fields += [_field]

        return self

    def add_fields(
            self,
            field_list: Union[Dict[Any, Any], Iterable[Iterable[Any, Any]]],
            checks: Optional[Callable[[Any], Any]] = bool,
            map_title: Optional[Callable[[Any], str]] = str,
            map_values: Optional[Callable[[Any], str]] = str,
            inline: bool = True
    ) -> Embed:
        """Add multiple fields from a list,
        dict or generator of fields with possible mapping.

        Parameters
        ----------
        field_list: Union[Dict[Any, Any], Iterable[Iterable[Any, Any]]]
            A iterable or generator of the fields to add.
            If the field_list type is a dictionary, will take items.
        checks: Optional[Callable[[Any], Any]]
            A filter function to remove embed fields.
        map_title: Optional[Callable[[Any], :class:`str`]]
            A transform function to change the titles.
        map_values: Optional[Callable[[Any], :class:`str`]]
            A transform function to change the values.
        inline: :class:`bool`
            Whether to create grid or each field on a new line.

        Raises
        ------
        EmbedFieldError:
            Raised when there are more than 25 fields in the embed

        Returns
        -------
        :class:`~pincer.objects.message.embed.Embed`
            The new embed object.
        """

        if isinstance(field_list, dict):
            field_list: Iterable[Iterable[Any, Any]] = field_list.items()

        for field_name, field_value in field_list:
            val = (
                map_values(field_value)
                if not isinstance(field_value, tuple)
                else map_values(*field_value)
            )

            if checks(val):
                self.add_field(
                    name=map_title(field_name),
                    value=val,
                    inline=inline
                )

        return self
