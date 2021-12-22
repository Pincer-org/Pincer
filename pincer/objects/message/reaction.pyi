from ...utils.api_object import APIObject as APIObject
from .emoji import Emoji as Emoji

class Reaction(APIObject):
    count: int
    me: bool
    emoji: Emoji
