from ...utils.api_object import APIObject as APIObject

class SessionStartLimit(APIObject):
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int
