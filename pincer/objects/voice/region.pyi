from ...utils.api_object import APIObject as APIObject

class VoiceRegion(APIObject):
    id: str
    name: str
    vip: bool
    optimal: bool
    deprecated: bool
    custom: bool
