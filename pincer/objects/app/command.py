# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
    Any,
    Awaitable,
    Callable,
    Generic,
    List,
    Optional,
    Union,
    TYPE_CHECKING,
    TypeVar,
)

from .command_types import AppCommandOptionType, AppCommandType
from ..app.throttle_scope import ThrottleScope
from ...commands.groups import Group, Subgroup
from ...objects.guild.channel import ChannelType
from ...utils.api_object import APIObject, GuildProperty
from ...utils.snowflake import Snowflake
from ...utils.types import Coro, choice_value_types
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils.types import APINullable

T = TypeVar("T")


@dataclass(repr=False)
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
    options: APINullable[List[AppCommandInteractionDataOption]] = MISSING


@dataclass(repr=False)
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

    def __post_init__(self):
        # APIObject __post_init_ causes issues by converting `value` to a string
        self.name = str(self.name)


@dataclass(repr=False)
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
        Choices for ``STRING``, ``INTEGER``, and ``NUMBER``
        types for the user to pick from, max 25
    options: APINullable[List[:class:`~pincer.objects.app.command.AppCommandOptionChoice`]]
        If the option is a subcommand or subcommand group type,
        this nested options will be the parameters
    """

    # noqa: E501
    type: AppCommandOptionType
    name: str
    description: str

    required: bool = False
    autocomplete: APINullable[bool] = MISSING
    choices: APINullable[List[AppCommandOptionChoice]] = MISSING
    options: APINullable[List[AppCommandOption]] = MISSING
    channel_types: APINullable[List[ChannelType]] = MISSING
    min_value: APINullable[Union[int, float]] = MISSING
    max_value: APINullable[Union[int, float]] = MISSING


@dataclass(repr=False)
class AppCommand(APIObject, GuildProperty):
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

    def __post_init__(self):
        super().__post_init__()

        if self.options is MISSING and self.type is AppCommandType.MESSAGE:
            self.options = []

    def __eq__(self, other: Union[AppCommand, InteractableStructure]):
        if isinstance(other, InteractableStructure):
            other = other.app

        # `description` and `options` are tested for equality with a custom check
        eq_props = ("type", "name", "guild_id", "default_permission", "options")

        eq = (
            self.__getattribute__(prop) == other.__getattribute__(prop)
            for prop in eq_props
        )

        return all(
            (
                *eq,
                self.description == other.description
                # If this command has a MISSING description, Discord would return
                # registered the command with the description ''
                or self.description is MISSING and not other.description,
            )
        )

    def __hash__(self):
        return hash((self.id, self.name, self.guild_id, self.type))

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


@dataclass(repr=False)
class InteractableStructure(Generic[T]):
    """Represents the structure of how the client saves the existing
    commands to registers. This is generic over Application Commands,
    Message Components, and Autocomplete.

    Attributes
    ----------
    call: :class:`~pincer.utils.types.Coro`
        The coroutine which should be called when the command gets
        executed.
    metadata: T
        The metadata for this command. |default| :data:`None`
    manager : Optional[Any]
        The manager for this interactable. |default| :data:`None`
    extensions: List[Callable[..., Awaitable[bool]]]
        List of extensions for this command. |default| :data:`[]`
    cooldown: :class:`int`
        Amount of times for cooldown |default| :data:`0`
    cooldown_scale: :class:`float`
        Search time for cooldown |default| :data:`60.0`
    cooldown_scope: :class:`~pincer.objects.app.throttle_scope.ThrottleScope`
        The type of cooldown |default| :data:`ThrottleScope.USER`
    """

    call: Coro

    metadata: Optional[T] = None
    manager: Optional[Any] = None
    extensions: List[Callable[..., Awaitable[bool]]] = field(
        default_factory=list
    )

    cooldown: int = 0
    cooldown_scale: float = 60.0
    cooldown_scope: ThrottleScope = ThrottleScope.USER

    group: APINullable[Group] = MISSING
    sub_group: APINullable[Subgroup] = MISSING

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.call(*args, **kwargs)
