from ...utils import APIObject as APIObject
from ..user.user import User as User
from typing import Optional

class Ban(APIObject):
    reason: Optional[str]
    user: User
