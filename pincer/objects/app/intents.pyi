from enum import IntEnum
from typing import Any

class Intents(IntEnum):
    NONE: int
    GUILDS: Any
    GUILD_MEMBERS: Any
    GUILD_BANS: Any
    GUILD_EMOJIS_AND_STICKERS: Any
    GUILD_INTEGRATIONS: Any
    GUILD_WEBHOOKS: Any
    GUILD_INVITES: Any
    GUILD_VOICE_STATES: Any
    GUILD_PRESENCES: Any
    GUILD_MESSAGES: Any
    GUILD_MESSAGE_REACTIONS: Any
    GUILD_MESSAGE_TYPING: Any
    DIRECT_MESSAGES: Any
    DIRECT_MESSAGE_REACTIONS: Any
    DIRECT_MESSAGE_TYPING: Any
    @staticmethod
    def all() -> int: ...
