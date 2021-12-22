from ...exceptions import PincerError as PincerError
from ...utils import APIObject as APIObject

class DiscordError(PincerError, APIObject):
    code: int
    message: str
