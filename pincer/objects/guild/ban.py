# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from pincer.utils import APIObject

if TYPE_CHECKING:
    from pincer.objects.user import User


@dataclass
class Ban(APIObject):
    """
    Representation of the Discord Ban object

    :param reason:
        The reason for the ban

    :param user:
        The banned user
    """
    reason: Optional[str]
    user: User
