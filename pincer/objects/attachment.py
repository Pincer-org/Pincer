# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional

from ..utils import APIObject, APINullable, MISSING, Snowflake


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

    content_type: APINullable[str] = MISSING
    height: APINullable[Optional[int]] = MISSING
    width: APINullable[Optional[int]] = MISSING
