# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional

from ...objects.guild.role import Role
from ...objects.user.user import User


@dataclass(repr=False)
class Mentionable:
    """
    Represents the Mentionable type

    user : Optional[:class:`~pincer.objects.user.user.User`]
        User object returned from a discord interaction
    role: Optional[:class:`~pincer.objects.guild.role.Role`]
        Role object returned from a discord interaction
    """

    user: Optional[User] = None
    role: Optional[Role] = None

    @property
    def is_user(self):
        """Returns true if the Mentionable object has a User"""
        return self.user is not None

    @property
    def is_role(self):
        """Returns true if the Mentionable object has a Role"""
        return self.role is not None
