# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Union, TYPE_CHECKING

from ...utils.types import Coro, choice_value_types
from ..app.throttle_scope import ThrottleScope
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING
from ...utils import types

if TYPE_CHECKING:
    from ...utils.conversion import convert
    from ...utils import extraction


class AppCommandType(IntEnum):
    """Defines the different types of application commands.
    """
    CHAT_INPUT = 1 #: Slash commands; a text-based command that shows up when a user types /
    USER = 2 #: A UI-based command that shows up when you right click or tap on a user
    MESSAGE = 3 #: A UI-based command that shows up when you right click or tap on a message


class AppCommandOptionType(IntEnum):
    """Represents a parameter type.
    """
    SUB_COMMAND = 1 #: The parameter will be a subcommand.
    SUB_COMMAND_GROUP = 2 #: The parameter will be a group of subcommands.
    STRING = 3 #: The parameter will be a string.
    INTEGER = 4 #: The parameter will be an integer/number. (-2^53 and 2^53)
    BOOLEAN = 5 #: The parameter will be a boolean.
    USER = 6 #: The parameter will be a Discord user object.
    CHANNEL = 7 #: The parameter will be a Discord channel object.
    ROLE = 8 #: The parameter will be a Discord role object.
    MENTIONABLE = 9 #: The parameter will be mentionable.
    NUMBER = 10  #: The parameter will be a float. (-2^53 and 2^53)

@dataclass
class AppCommandInteractionDataOption(APIObject):
    """Represents a Discord Application Command Interaction Data Option

    Attributes
    ----------
    name: :class:`str`
        The name of the parameter
    value: :class:`str`
        The value of the pair
    type: :data:`~pincer.utils.types.APINullable`\\[:class:`str`]
        Value of application command option type
    options: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.List`\\[:data:`~pincer.objects.app.command.AppCommandInteractionDataOption`]]
        Present if this option is a group or subcommand
    """
    name: str
    value: types.APINullable[str] = MISSING
    type: types.APINullable[AppCommandOptionType] = MISSING
    options: types.APINullable[
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
    """Represents a Discord Application Command Option Choice object

    Attributes
    ----------
    name: :class:`str`
        1-100 character choice name
    value: :data:`~typing.Union`\\[:data:`~pincer.utils.types.choice_value_types`]
        Value of the choice, up to 100 characters if string
    """
    name: str
    value: Union[choice_value_types]


@dataclass
class AppCommandOption(APIObject):
    """Represents a Discord Application Command Option object

    Attributes
    ----------
    type: :class:`~pincer.objects.AppCommandOptionType`
        The type of option
    name: :class:`str`
        1-32 lowercase character name matching `^[\\w-]{1,32}$`
    description: :class:`str`
        1-100 character description
    required: :data:`~pincer.utils.types.APINullable`\\[:class:`bool`]
        If the parameter is required or optional |default| :data:`False`
    choices: :data:`~pincer.utils.types.APINullable`\\[:data:`typing.List`\\[:class:`~pincer.objects.app.command.AppCommandOptionChoice`]]
        Choices for `STRING`, `INTEGER`, and `NUMBER`
        types for the user to pick from, max 25
    options: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.List`\\[:class:`~pincer.objects.app.command.AppCommandOptionChoice`]]
        If the option is a subcommand or subcommand group type,
        this nested options will be the parameters
    """
    type: AppCommandOptionType
    name: str
    description: str

    required: types.APINullable[bool] = False
    choices: types.APINullable[List[AppCommandOptionChoice]] = MISSING
    options: types.APINullable[List[AppCommandOption]] = MISSING

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
    """Represents a Discord Application Command object

    Attributes
    ----------
    type: :class:`~pincer.objects.app.command.AppCommandType`
        The type of command, defaults ``1`` if not set
    name: :class:`str`
        1-32 character name
    description: :class:`str`
        1-100 character description for ``CHAT_INPUT`` commands,
        empty string for ``USER`` and ``MESSAGE`` commands
    id: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        Unique id of the command
    version: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        Autoincrementing version identifier updated during substantial
        record changes
    application_id: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        Unique id of the parent application
    options: :data:`~pincer.utils.types.APINullable`\\[:class:`~typing.List`\\[:class:`~pincer.objects.app.command.AppCommandOption`]]
        The parameters for the command, max 25
    guild_id: :data:`~pincer.utils.types.APINullable`\\[:class:`~pincer.utils.snowflake.Snowflake`]
        Guild id of the command, if not global
    default_permission: :data:`~pincer.utils.types.APINullable`\\[:class:`bool`]
        Whether the command is enabled by default
        when the app is added to a guild
    """
    type: AppCommandType
    name: str
    description: str

    id: types.APINullable[Snowflake] = MISSING
    version: types.APINullable[Snowflake] = MISSING
    application_id: types.APINullable[Snowflake] = MISSING
    options: types.APINullable[List[AppCommandOption]] = MISSING
    guild_id: types.APINullable[Snowflake] = MISSING
    default_permission: types.APINullable[bool] = True

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
            option != extraction.get_index(self.options, idx)
            for idx, option in enumerate(other.options)
        )

    def __hash__(self):
        return hash((self.id, self.name, self.description))

    def add_option(self, option: AppCommandOption):
        """Add a new option field to the current application command.

        Parameters
        ----------
        option :
            The option which will be appended.
        """
        if self.options:
            self.options.append(option)
        else:
            self.options = [option]


@dataclass
class ClientCommandStructure:
    """Represents the structure of how the client saves the existing
    commands in the register.

    Attributes
    ----------
    app: :class:`~pincer.objects.app.command.AppCommand`
        The command application.
    call: :class:`~pincer.utils.types.Coro`
        The coroutine which should be called when the command gets
        executed.
    cooldown: :class:`int`
        Amount of times for cooldown
    cooldown_scale: :class:`float`
        Search time for cooldown
    cooldown_scope: :class:`~pincer.objects.app.throttle_scope.ThrottleScope`
        The type of cooldown
    """
    app: AppCommand
    call: Coro
    cooldown: int
    cooldown_scale: float
    cooldown_scope: ThrottleScope
