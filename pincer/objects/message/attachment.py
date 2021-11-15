# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Optional

    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


@dataclass
class Attachment(APIObject):
    """Represents a Discord Attachment object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Attachment id
    filename: :class:`str`
        Name of file attached
    content_type: :class:`int`
        The attachment's data type
    size: :class:`str`
        Size of file in bytes
    url: :class:`str`
        Source url of file
    proxy_url: APINullable[:class:`str`]
        A proxied url of file
    height: APINullable[Optional[:class:`int`]]
        Height of file (if image)
    width: APINullable[Optional[:class:`int`]]
        Width of file (if image)
    """
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str

    content_type: APINullable[str] = MISSING
    height: APINullable[Optional[int]] = MISSING
    width: APINullable[Optional[int]] = MISSING
