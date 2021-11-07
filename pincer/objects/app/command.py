# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, TYPE_CHECKING

from .command_types import AppCommandOptionType, AppCommandType
from ...utils.api_object import APIObject
from ...utils.conversion import convert
from ...utils.extraction import get_index
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ..app.throttle_scope import ThrottleScope
    from ...utils.types import APINullable, Coro, choice_value_types


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
    :param default_member_permissions:
        # TODO: Fix docs for this when discord has implemented it.
    :param dm_permission:
        # TODO: Fix docs for this when discord has implemented it.
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
