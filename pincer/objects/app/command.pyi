from ...objects.guild.channel import ChannelType as ChannelType
from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, Coro as Coro, MISSING as MISSING, choice_value_types as choice_value_types
from ..app.throttle_scope import ThrottleScope as ThrottleScope
from .command_types import AppCommandOptionType as AppCommandOptionType, AppCommandType as AppCommandType
from typing import List, Union

class AppCommandInteractionDataOption(APIObject):
    name: str
    value: APINullable[str]
    type: APINullable[AppCommandOptionType]
    options: APINullable[List[AppCommandInteractionDataOption]]

class AppCommandOptionChoice(APIObject):
    name: str
    value: choice_value_types

class AppCommandOption(APIObject):
    type: AppCommandOptionType
    name: str
    description: str
    required: bool
    autocomplete: APINullable[bool]
    choices: APINullable[List[AppCommandOptionChoice]]
    options: APINullable[List[AppCommandOption]]
    channel_types: APINullable[List[ChannelType]]
    min_value: APINullable[Union[int, float]]
    max_value: APINullable[Union[int, float]]

class AppCommand(APIObject, GuildProperty):
    type: AppCommandType
    name: str
    description: str
    id: APINullable[Snowflake]
    version: APINullable[Snowflake]
    application_id: APINullable[Snowflake]
    options: APINullable[List[AppCommandOption]]
    guild_id: APINullable[Snowflake]
    default_permission: APINullable[bool]
    default_member_permissions: APINullable[None]
    dm_permission: APINullable[None]
    def __post_init__(self) -> None: ...
    def __eq__(self, other: Union[AppCommand, ClientCommandStructure]): ...
    def __hash__(self): ...
    def add_option(self, option: AppCommandOption): ...

class ClientCommandStructure:
    app: AppCommand
    call: Coro
    cooldown: int
    cooldown_scale: float
    cooldown_scope: ThrottleScope
