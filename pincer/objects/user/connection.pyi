from ...utils.api_object import APIObject as APIObject
from ...utils.types import APINullable as APINullable
from .integration import Integration as Integration
from .user import VisibilityType as VisibilityType
from typing import List

class Connection(APIObject):
    id: str
    name: str
    type: str
    verified: bool
    friend_sync: bool
    show_activity: bool
    visibility: VisibilityType
    revoked: APINullable[bool]
    integrations: APINullable[List[Integration]]
