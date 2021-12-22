from ...utils import APIObject as APIObject

class ActivityJoinEvent(APIObject):
    secret: str

class ActivitySpectateEvent(APIObject):
    secret: str
