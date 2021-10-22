# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from enum import IntEnum


class AppCommandType(IntEnum):
    """
    Defines the different types of application commands.

    :param CHAT_INPUT:
        Slash commands; a text-based command that shows up when a user
        types /

    :param USER:
        A UI-based command that shows up when you right click or tap on
        a user

    :param MESSAGE:
        A UI-based command that shows up when you right click or tap on
        a message
    """
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class AppCommandOptionType(IntEnum):
    """
    Represents a parameter type.

    :param SUB_COMMAND:
        The parameter will be a subcommand.

    :param SUB_COMMAND_GROUP:
        The parameter will be a group of subcommands.

    :param STRING:
        The parameter will be a string.

    :param INTEGER:
        The parameter will be an integer/number. (-2^53 and 2^53)

    :param BOOLEAN:
        The parameter will be a boolean.

    :param USER:
        The parameter will be a Discord user object.

    :param CHANNEL:
        The parameter will be a Discord channel object.

    :param ROLE:
        The parameter will be a Discord role object.

    :param MENTIONABLE:
        The parameter will be mentionable.

    :param NUMBER:
        The parameter will be a float. (-2^53 and 2^53)
    """
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4  # 54-bit
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10  # 54-bit
