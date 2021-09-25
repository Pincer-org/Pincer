# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional

from .user import User
from ..utils import APIObject


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
