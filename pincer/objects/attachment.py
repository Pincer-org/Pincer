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

from dataclasses import dataclass
from typing import Optional

from pincer.utils.api_object import APIObject
from pincer.utils.constants import MISSING, OptionallyProvided
from pincer.utils.snowflake import Snowflake


@dataclass
class Attachment(APIObject):
    """Represents a Discord Attachment object

    :param id:
        attachment id

    :param filename:
        name of file attached

    :param content_type:
        the attachment's data type

    :param size:
        size of file in bytes

    :param url:
        source url of file

    :param proxy_url:
        a proxied url of file

    :param height:
        height of file (if image)

    :param width:
        width of file (if image)
    """
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str

    content_type: OptionallyProvided[str] = MISSING
    height: OptionallyProvided[Optional[int]] = MISSING
    width: OptionallyProvided[Optional[int]] = MISSING
