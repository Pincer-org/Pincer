# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils import APIObject

if TYPE_CHECKING:
    from ...utils import Snowflake


@dataclass
class Overwrite(APIObject):
    """
    Represents a Discord Overwrite object

    :param id:
        role or user id

    :param type:
        either 0 (role) or 1 (member)

    :param allow:
        permission bit set

    :param deny:
        permission bit set
    """
    id: Snowflake
    type: int
    allow: str
    deny: str
