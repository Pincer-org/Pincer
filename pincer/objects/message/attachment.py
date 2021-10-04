# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ...utils.api_object import APIObject
from ...utils.types import MISSING
from ...utils import types
from ...utils.snowflake import Snowflake


@dataclass
class Attachment(APIObject):
    """
    Represents a Discord Attachment object

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

    content_type: types.APINullable[str] = MISSING
    height: types.APINullable[Optional[int]] = MISSING
    width: types.APINullable[Optional[int]] = MISSING
