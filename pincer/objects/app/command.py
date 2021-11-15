# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, TYPE_CHECKING

from .command_types import AppCommandOptionType, AppCommandType
from ...utils.api_object import APIObject
from ...utils.conversion import convert
from ...utils.snowflake import Snowflake
from ...utils.types import Coro, choice_value_types
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils.types import APINullable
    from ..app.throttle_scope import ThrottleScope


@dataclass
class AppCommandInteractionDataOption(APIObject):
    """Represents a Discord Application Command Interaction Data Option

    Attributes
    ----------
    name: :class:`str`
        The name of the parameter
    value: :class:`str`
        The value of the pair
    type: APINullable[:class:`str`]
        Value of application command option type
    options: APINullable[List[:data:`~pincer.objects.app.command.AppCommandInteractionDataOption`]]
        Present if this option is a group or subcommand
    """
    # noqa: E501
    name: str
    value: APINullable[str] = MISSING
    type: APINullable[AppCommandOptionType] = MISSING
    options: APINullable[
        List[AppCommandInteractionDataOption]] = MISSING


@dataclass
class AppCommandOptionChoice(APIObject):
    """Represents a Discord Application Command Option Choice object

    Attributes
    ----------
    name: :class:`str`
        1-100 character choice name
    value: Union[:data:`~pincer.utils.types.choice_value_types`]
        Value of the choice, up to 100 characters if string
    """
    name: str
    value: choice_value_types


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
    required: APINullable[:class:`bool`]
        If the parameter is required or optional |default| :data:`False`
    choices: APINullable[List[:class:`~pincer.objects.app.command.AppCommandOptionChoice`]]
        Choices for `STRING`, `INTEGER`, and `NUMBER`
        types for the user to pick from, max 25
    options: APINullable[List[:class:`~pincer.objects.app.command.AppCommandOptionChoice`]]
        If the option is a subcommand or subcommand group type,
        this nested options will be the parameters
    """
    # noqa: E501
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
    id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Unique id of the command
    version: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Auto-incrementing version identifier updated during substantial
        record changes
    application_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Unique id of the parent application
    options: APINullable[List[:class:`~pincer.objects.app.command.AppCommandOption`]]
        The parameters for the command, max 25
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Guild id of the command, if not global
    default_permission: APINullable[:class:`bool`]
        Whether the command is enabled by default
        when the app is added to a guild
    """
    # noqa: E501
    type: AppCommandType
    name: str
    description: str

    id: APINullable[Snowflake] = MISSING
    version: APINullable[Snowflake] = MISSING
    application_id: APINullable[Snowflake] = MISSING
    options: APINullable[List[AppCommandOption]] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    default_permission: APINullable[bool] = True
    default_member_permissions: APINullable[None] = None
    dm_permission: APINullable[None] = None

    _eq_props = [
        "type", "name", "description", "guild_id", "default_permission",
        "options"
    ]

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)
        self.version = convert(self.version, Snowflake.from_string)
        self.type = AppCommandType(self.type)
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

        return all(
            self.__getattribute__(prop) == other.__getattribute__(prop)
            for prop in self._eq_props
        )

    def __hash__(self):
        return hash((self.id, self.name, self.description, self.guild_id))

    def add_option(self, option: AppCommandOption):
        """Add a new option field to the current application command.

        Parameters
        ----------
        option : :class:`~pincer.objects.app.command.AppCommandOption`
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
