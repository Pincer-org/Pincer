# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Union, TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.conversion import convert
from ...utils.extraction import get_index
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ..app.throttle_scope import ThrottleScope
    from ...utils.types import APINullable, Coro, choice_value_types


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


@dataclass
class AppCommandInteractionDataOption(APIObject):
    """
    Represents a Discord Application Command Interaction Data Option

    :param name:
        the name of the parameter

    :param type:
        value of application command option type

    :param value:
        the value of the pair

    :param options:
        present if this option is a group or subcommand
    """
    name: str
    value: APINullable[str] = MISSING
    type: APINullable[AppCommandOptionType] = MISSING
    options: APINullable[
        List[AppCommandInteractionDataOption]] = MISSING

    def __post_init__(self):
        self.type = convert(self.type, AppCommandOptionType)
        self.options = convert(
            self.options,
            AppCommandInteractionDataOption.from_dict,
            AppCommandInteractionDataOption
        )


@dataclass
class AppCommandOptionChoice(APIObject):
    """
    Represents a Discord Application Command Option Choice object

    :param name:
        1-100 character choice name

    :param value:
        value of the choice, up to 100 characters if string
    """
    name: str
    value: Union[choice_value_types]


@dataclass
class AppCommandOption(APIObject):
    """
    Represents a Discord Application Command Option object

    :param type:
        the type of option

    :param name:
        1-32 lowercase character name matching `^[\\w-]{1,32}$`

    :param description:
        1-100 character description

    :param required:
        if the parameter is required or optional--default `False`

    :param choices:
        choices for `STRING`, `INTEGER`, and `NUMBER`
        types for the user to pick from, max 25

    :param options:
        if the option is a subcommand or subcommand group type,
        this nested options will be the parameters
    """
    type: AppCommandOptionType
    name: str
    description: str

    required: APINullable[bool] = False
    choices: APINullable[List[AppCommandOptionChoice]] = MISSING
    options: APINullable[List[AppCommandOption]] = MISSING

    def __post_init__(self):
        self.type = AppCommandOptionType(self.type)
        self.choices = convert(
            self.choices,
            AppCommandOptionChoice.from_dict,
            AppCommandOptionChoice
        )
        self.options = convert(
            self.options,
            AppCommandOption.from_dict,
            AppCommandOption
        )


@dataclass
class AppCommand(APIObject):
    """
    Represents a Discord Application Command object

    :param id:
        unique id of the command

    :param type:
        the type of command, defaults `1` if not set

    :param application_id:
        unique id of the parent application

    :param guild_id:
        guild id of the command, if not global

    :param name:
        1-32 character name

    :param description:
        1-100 character description for `CHAT_INPUT` commands,
        empty string for `USER` and `MESSAGE` commands

    :param options:
        the parameters for the command, max 25

    :param default_permission:
        whether the command is enabled by default
        when the app is added to a guild

    :param version:
        autoincrementing version identifier updated during substantial
        record changes
    """
    type: AppCommandType
    name: str
    description: str

    id: APINullable[Snowflake] = MISSING
    version: APINullable[Snowflake] = MISSING
    application_id: APINullable[Snowflake] = MISSING
    options: APINullable[List[AppCommandOption]] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    default_permission: APINullable[bool] = True

    _eq_props = [
        "type", "name", "description", "guild_id", "default_permission"
    ]

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)
        self.version = convert(self.version, Snowflake.from_string)
        self.application_id = convert(
            self.application_id, Snowflake.from_string
        )

        self.options = convert(
            self.options,
            AppCommandOption.from_dict,
            AppCommandOption
        )
        self.guild_id = convert(self.guild_id, Snowflake.from_string)

        self.options = [] if self.options is MISSING else self.options

    def __eq__(self, other: Union[AppCommand, ClientCommandStructure]):
        if isinstance(other, ClientCommandStructure):
            other = other.app

        is_equal = all(
            self.__getattribute__(prop) == other.__getattribute__(prop)
            for prop in self._eq_props
        )

        if (
                (self.options is MISSING and other.options is not MISSING)
                or (self.options is not MISSING and other.options is MISSING)
                and not is_equal
        ):
            return False

        if len(other.options) != len(self.options):
            return False

        return not any(
            option != get_index(self.options, idx)
            for idx, option in enumerate(other.options)
        )

    def __hash__(self):
        return hash((self.id, self.name, self.description))

    def add_option(self, option: AppCommandOption):
        """
        Add a new option field to the current application command.

        :param option: The option which will be appended.
        """
        if self.options:
            self.options.append(option)
        else:
            self.options = [option]


@dataclass
class ClientCommandStructure:
    """
    Represents the structure of how the client saves the existing
    commands in the register.

    :param app:
        The command application.

    :param call:
        The coroutine which should be called when the command gets
        executed.
    """
    app: AppCommand
    call: Coro
    cooldown: int
    cooldown_scale: float
    cooldown_scope: ThrottleScope
