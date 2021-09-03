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

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum, auto
from typing import Optional

from pincer.utils.api_object import APIObject

@dataclass
class EmbedFooter:
    """
    Representation of the Embed Footer class

    :param text: Footer text
    :param icon_url: Url of the footer icon
    :param proxy_icon_url: A proxied url of the footer icon
    """

    text: str
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None

@dataclass
class EmbedImage:
    """
    Representation of the Embed Image class

    :param url: Source url of the image
    :param proxy_url: A proxied url of the image
    :param height: Height of the image
    :param width: Width of the image
    """
    
    url: Optional[str] = None
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

@dataclass
class EmbedThumbnail:
    """
    Representation of the Embed Thumbnail class

    :param url: Source url of the thumbnail
    :param proxy_url: A proxied url of the thumbnail
    :param height: Height of the thumbnail
    :param width: Width of the thumbnail
    """

    url: Optional[str] = None
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

@dataclass
class EmbedVideo:
    """
    Representation of the Embed Video class

    :param url: Source url of the video
    :param proxy_url: A proxied url of the video
    :param height: Height of the video
    :param width: Width of the video
    """
    url: Optional[str] = None
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None

@dataclass
class EmbedProvider:
    """
    :param name: Name of the provider
    :param url: Url of the provider
    """
    name: Optional[str] = None
    url: Optional[str] = None

@dataclass
class EmbedAuthor:
    """
    Representation of the Embed Author class
    
    :param name: Name of the author
    :param url: Url of the author
    :param icon_url: Url of the author icon
    :param proxy_icon_url: A proxied url of the author icon
    """
    name: Optional[str] = None
    url: Optional[str] = None
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None

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
    inline: Optional[bool] = None 

@dataclass
class Embed(APIObject):
    """
    Representation of the discord Embed class

    :param title: Embed title.
    :param description: Embed description.
    :param url: Embed url.
    :param timestamp: Timestamp of embed content in ISO format.
    :param color: Embed color code.
    :param footer: Footer information.
    :param image: Image information.
    :param thumbnail: Thumbnail information.
    :param video: Video information.
    :param provider: Provider information.
    :param author: Author information.
    :param fields: Fields information.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    fields: Optional[list[EmbedField]] = None

    def set_timestamp(self, time: datetime):
        self.timestamp = time.isoformat()