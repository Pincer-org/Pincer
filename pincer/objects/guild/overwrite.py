# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .permissions import Permissions
from ...utils import APIObject

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


@dataclass(repr=False)
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

    @property
    def permissions(self) -> Permissions:
        """Returns the permissions for this overwrite"""
        return Permissions.from_ints(int(self.allow), int(self.deny))
