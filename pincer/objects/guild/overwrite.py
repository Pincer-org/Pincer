# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils import APIObject

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


@dataclass
class Overwrite(APIObject):
    """Represents a Discord Overwrite object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Role or user id
    type: :class:`int`
        Either 0 (role) or 1 (member)
    allow: :class:`str`
        Permission bit set
    deny: :class:`str`
        Permission bit set
    """
    id: Snowflake
    type: int
    allow: str
    deny: str
