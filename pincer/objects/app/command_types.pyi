from enum import IntEnum

class AppCommandType(IntEnum):
    CHAT_INPUT: int
    USER: int
    MESSAGE: int

class AppCommandOptionType(IntEnum):
    SUB_COMMAND: int
    SUB_COMMAND_GROUP: int
    STRING: int
    INTEGER: int
    BOOLEAN: int
    USER: int
    CHANNEL: int
    ROLE: int
    MENTIONABLE: int
    NUMBER: int
