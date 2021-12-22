from ...objects.guild.role import Role as Role
from ...objects.user.user import User as User
from typing import Optional

class Mentionable:
    user: Optional[User]
    role: Optional[Role]
    @property
    def is_user(self): ...
    @property
    def is_role(self): ...
