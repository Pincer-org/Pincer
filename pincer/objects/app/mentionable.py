# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass


from ...objects.guild.role import Role
from ...objects.user.user import User
from ...utils.types import MISSING, APINullable


# Inspired by Rust (🚀) enums 🚀
@dataclass
class Mentionable:
    user: APINullable[User] = MISSING
    role: APINullable[Role] = MISSING

    @property
    def is_user(self):
        return self.user is not MISSING

    @property
    def is_role(self):
        return self.role is not MISSING
