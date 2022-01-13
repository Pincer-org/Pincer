# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
import re
from asyncio import iscoroutinefunction, gather
from functools import partial
from inspect import Signature, isasyncgenfunction, _empty
from typing import TYPE_CHECKING, TypeVar, Union, List, ValuesView


from . import __package__
from ..commands.arg_types import (
    ChannelTypes,
    CommandArg,
    Description,
    Choices,
    MaxValue,
    MinValue,
)
from ..commands.groups import Group, Subgroup
from ..utils.snowflake import Snowflake
from ..exceptions import (
    CommandIsNotCoroutine,
    CommandAlreadyRegistered,
    TooManyArguments,
    InvalidArgumentAnnotation,
    CommandDescriptionTooLong,
    InvalidCommandGuild,
    InvalidCommandName,
    ForbiddenError,
)
from ..objects import (
    ThrottleScope,
    AppCommand,
    Role,
    User,
    Channel,
    Guild,
    Mentionable,
    MessageContext,
)
from ..objects.app import (
    AppCommandOptionType,
    AppCommandOption,
    ClientCommandStructure,
    AppCommandType,
)
from ..utils import should_pass_ctx
from ..utils.signature import get_signature_and_params
from ..utils.types import MISSING
from ..utils.types import Singleton

if TYPE_CHECKING:
    from typing import Any, Optional, Dict

REGULAR_COMMAND_NAME_REGEX = re.compile(r"[\w\- ]{1,32}$")
CHAT_INPUT_COMMAND_NAME_REGEX = re.compile(r"^[a-z0-9_-]{1,32}$")

_log = logging.getLogger(__package__)

_options_type_link = {
    Signature.empty: AppCommandOptionType.STRING,
    str: AppCommandOptionType.STRING,
    int: AppCommandOptionType.INTEGER,
    bool: AppCommandOptionType.BOOLEAN,
    float: AppCommandOptionType.NUMBER,
    User: AppCommandOptionType.USER,
    Channel: AppCommandOptionType.CHANNEL,
    Role: AppCommandOptionType.ROLE,
    Mentionable: AppCommandOptionType.MENTIONABLE,
}

if TYPE_CHECKING:
    from ..client import Client

T = TypeVar("T")


def command(
    func=None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = "Description not set",
    enable_default: Optional[bool] = True,
    guild: Union[Snowflake, int, str] = None,
    cooldown: Optional[int] = 0,
    cooldown_scale: Optional[float] = 60.0,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
    parent: Optional[Union[Group, Subgroup]] = None
):
    """A decorator to create a slash command to register and respond to
    with the discord API from a function.

    str - String
    int - Integer
    bool - Boolean
    float - Number
    pincer.objects.User - User
    pincer.objects.Channel - Channel
    pincer.objects.Role - Role
    pincer.objects.Mentionable - Mentionable

    .. code-block:: python3

        class Bot(Client):
            @command(
                name="test",
                description="placeholder"
            )
            async def test_command(
                self,
                ctx: MessageContext,
                amount: int,
                name: CommandArg[
                    str,
                    Description("Do something cool"),
                    Choices(Choice("first value", 1), 5)
                ],
                optional_int: CommandArg[
                    int,
                    MinValue(10),
                    MaxValue(100),
                ] = 50
            ):
                return Message(
                    f"You chose {amount}, {name}, {letter}",
                    flags=InteractionFlags.EPHEMERAL
                )


    References from above:
        :class:`~pincer.client.Client`,
        :class:`~pincer.objects.message.message.Message`,
        :class:`~pincer.objects.message.context.MessageContext`,
        :class:`~pincer.objects.app.interaction_flags.InteractionFlags`,
        :class:`~pincer.commands.arg_types.Choices`,
        :class:`~pincer.commands.arg_types.Choice`,
        :class:`typing_extensions.Annotated` (Python 3.8),
        :class:`typing.Annotated` (Python 3.9+),
        :class:`~pincer.commands.arg_types.CommandArg`,
        :class:`~pincer.commands.arg_types.Description`,
        :class:`~pincer.commands.arg_types.MinValue`,
        :class:`~pincer.commands.arg_types.MaxValue`


    Parameters
    ----------
    name : Optional[:class:`str`]
        The name of the command |default| :data:`None`
    description : Optional[:class:`str`]
        The description of the command |default| ``Description not set``
    enable_default : Optional[:class:`bool`]
        Whether the command is enabled by default |default| :data:`True`
    guild : Optional[Union[:class:`~pincer.utils.snowflake.Snowflake`, :class:`int`, :class:`str`]]
        What guild to add it to (don't specify for global) |default| :data:`None`
    cooldown : Optional[:class:`int`]
        The amount of times in the cooldown_scale the command can be invoked
        |default| ``0``
    cooldown_scale : Optional[:class:`float`]
        The 'checking time' of the cooldown |default| ``60``
    cooldown_scope : :class:`~pincer.objects.app.throttle_scope.ThrottleScope`
        What type of cooldown strategy to use |default| :attr:`ThrottleScope.USER`

    Raises
    ------
    CommandIsNotCoroutine
        If the command function is not a coro
    InvalidCommandName
        If the command name does not follow the regex ``^[\\w-]{1,32}$``
    InvalidCommandGuild
        If the guild id is invalid
    CommandDescriptionTooLong
        Descriptions max 100 characters
        If the annotation on an argument is too long (also max 100)
    CommandAlreadyRegistered
        If the command already exists
    TooManyArguments
        Max 25 arguments to pass for commands
    InvalidArgumentAnnotation
        Annotation amount is max 25,
        Not a valid argument type,
        Annotations must consist of name and value
    """  # noqa: E501
    if func is None:
        return partial(
            command,
            name=name,
            description=description,
            enable_default=enable_default,
            guild=guild,
            cooldown=cooldown,
            cooldown_scale=cooldown_scale,
            cooldown_scope=cooldown_scope,
            parent=parent
        )

    cmd = name or func.__name__

    if not re.match(CHAT_INPUT_COMMAND_NAME_REGEX, cmd):
        raise InvalidCommandName(
            f"Command `{cmd}` doesn't follow the name requirements."
            " Ensure to match the following regex:"
            f" {CHAT_INPUT_COMMAND_NAME_REGEX.pattern}"
        )

    options: List[AppCommandOption] = []

    signature, params = get_signature_and_params(func)
    pass_context = should_pass_ctx(signature, params)

    if len(params) > (25 + pass_context):
        cmd = name or func.__name__
        raise TooManyArguments(
            f"Command `{cmd}` (`{func.__name__}`) can only have 25 "
            f"arguments (excluding the context and self) yet {len(params)} "
            "were provided!"
        )

    for idx, param in enumerate(params):
        if idx == 0 and pass_context:
            continue

        sig = signature[param]

        annotation, required = sig.annotation, sig.default is _empty

        # ctx is type MessageContext but should not be included in the
        # slash command
        if annotation == MessageContext and idx == 1:
            return

        argument_type = None
        if type(annotation) is CommandArg:
            argument_type = annotation.command_type
        # isinstance and type don't work for Annotated. This is the best way 💀
        elif hasattr(annotation, "__metadata__"):
            # typing.get_origin doesn't work in 3.9+ for some reason. Maybe they forgor
            # to implement it.
            argument_type = annotation.__origin__

        if not argument_type:
            if annotation in _options_type_link:
                options.append(
                    AppCommandOption(
                        type=_options_type_link[annotation],
                        name=param,
                        description="Description not set",
                        required=required,
                    )
                )
                continue

            # TODO: Write better exception
            raise InvalidArgumentAnnotation(
                "Type must be Annotated or other valid type"
            )

        command_type = _options_type_link[argument_type]

        def get_arg(t: T) -> APINullable[T]:
            if type(annotation) is CommandArg:
                return annotation.get_arg(t)
            elif hasattr(annotation, "__metadata__"):
                for obj in annotation.__metadata__:
                    if isinstance(obj, t):
                        return obj.get_payload()
                return MISSING

        argument_description = (
            get_arg(Description) or "Description not set"
        )

        choices = get_arg(Choices)

        if choices is not MISSING and argument_type not in {
            int,
            float,
            str,
        }:
            raise InvalidArgumentAnnotation(
                "Choice type is only allowed for str, int, and float"
            )
        if choices is not MISSING:
            for choice in choices:
                if (
                    isinstance(choice.value, int)
                    and argument_type is float
                ):
                    continue
                if not isinstance(choice.value, argument_type):
                    raise InvalidArgumentAnnotation(
                        "Choice value must match the command type"
                    )

        channel_types = get_arg(ChannelTypes)
        if (
            channel_types is not MISSING
            and argument_type is not Channel
        ):
            raise InvalidArgumentAnnotation(
                "ChannelTypes are only available for Channels"
            )

        max_value = get_arg(MaxValue)
        min_value = get_arg(MinValue)

        for i, value in enumerate((min_value, max_value)):
            if (
                value is not MISSING
                and argument_type is not int
                and argument_type is not float
            ):
                t = ("MinValue", "MaxValue")
                raise InvalidArgumentAnnotation(
                    f"{t[i]} is only available for int and float"
                )

        options.append(
            AppCommandOption(
                type=command_type,
                name=param,
                description=argument_description,
                required=required,
                choices=choices,
                channel_types=channel_types,
                max_value=max_value,
                min_value=min_value,
            )
        )

    # Discord API returns MISSING for options when there are 0. Options is set MISSING
    # so equality checks later work properly.
    if not options:
        options = MISSING

    return register_command(
        func=func,
        app_command_type=AppCommandType.CHAT_INPUT,
        name=name,
        description=description,
        enable_default=enable_default,
        guild=guild,
        cooldown=cooldown,
        cooldown_scale=cooldown_scale,
        cooldown_scope=cooldown_scope,
        command_options=options,
        parent=parent
    )


def user_command(
    func=None,
    *,
    name: Optional[str] = None,
    enable_default: Optional[bool] = True,
    guild: Union[Snowflake, int, str] = None,
    cooldown: Optional[int] = 0,
    cooldown_scale: Optional[float] = 60,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
):
    """A decorator to create a user command registering and responding
    to the Discord API from a function.

    .. code-block:: python3

         class Bot(Client):
             @user_command
             async def test_user_command(
                 self,
                 ctx: MessageContext,
                 user: User,
                 member: GuildMember
             ):
                 if not member:
                     # member is missing if this is a DM
                     # This bot doesn't like being DMed, so it won't respond
                     return

                 return f"Hello {user.name}, this is a Guild."


    References from above:
        :class:`~client.Client`,
        :class:`~objects.message.context.MessageContext`,
        :class:`~objects.user.user.User`,
        :class:`~objects.guild.member.GuildMember`,


    Parameters
    ----------
    name : Optional[:class:`str`]
        The name of the command |default| :data:`None`
    enable_default : Optional[:class:`bool`]
        Whether the command is enabled by default |default| :data:`True`
    guild : Optional[Union[:class:`~pincer.utils.snowflake.Snowflake`, :class:`int`, :class:`str`]]
        What guild to add it to (don't specify for global) |default| :data:`None`
    cooldown : Optional[:class:`int`]
        The amount of times in the cooldown_scale the command can be invoked
        |default| ``0``
    cooldown_scale : Optional[:class:`float`]
        The 'checking time' of the cooldown |default| ``60``
    cooldown_scope : :class:`~pincer.objects.app.throttle_scope.ThrottleScope`
        What type of cooldown strategy to use |default| :attr:`ThrottleScope.USER`

    Raises
    ------
    CommandIsNotCoroutine
        If the command function is not a coro
    InvalidCommandName
        If the command name does not follow the regex ``^[\\w-]{1,32}$``
    InvalidCommandGuild
        If the guild id is invalid
    CommandDescriptionTooLong
        Descriptions max 100 characters
        If the annotation on an argument is too long (also max 100)
    CommandAlreadyRegistered
        If the command already exists
    InvalidArgumentAnnotation
        Annotation amount is max 25,
        Not a valid argument type,
        Annotations must consist of name and value
    """  # noqa: E501
    return register_command(
        func=func,
        app_command_type=AppCommandType.USER,
        name=name,
        enable_default=enable_default,
        guild=guild,
        cooldown=cooldown,
        cooldown_scale=cooldown_scale,
        cooldown_scope=cooldown_scope,
    )


def message_command(
    func=None,
    *,
    name: Optional[str] = None,
    enable_default: Optional[bool] = True,
    guild: Union[Snowflake, int, str] = None,
    cooldown: Optional[int] = 0,
    cooldown_scale: Optional[float] = 60,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
):
    """A decorator to create a user command to register and respond
    to the Discord API from a function.

    .. code-block:: python3

        class Bot(Client):
            @user_command
            async def test_message_command(
                self,
                ctx: MessageContext,
                message: UserMessage,
            ):
                return message.content


    References from above:
        :class:`~client.Client`,
        :class:`~objects.message.context.MessageContext`,
        :class:`~objects.message.message.UserMessage`,
        :class:`~objects.user.user.User`,
        :class:`~objects.guild.member.GuildMember`,


    Parameters
    ----------
    name : Optional[:class:`str`]
        The name of the command |default| :data:`None`
    enable_default : Optional[:class:`bool`]
        Whether the command is enabled by default |default| :data:`True`
    guild : Optional[Union[:class:`~pincer.utils.snowflake.Snowflake`, :class:`int`, :class:`str`]]
        What guild to add it to (don't specify for global) |default| :data:`None`
    cooldown : Optional[:class:`int`]
        The amount of times in the cooldown_scale the command can be invoked
        |default| ``0``
    cooldown_scale : Optional[:class:`float`]
        The 'checking time' of the cooldown |default| ``60``
    cooldown_scope : :class:`~pincer.objects.app.throttle_scope.ThrottleScope`
        What type of cooldown strategy to use |default| :attr:`ThrottleScope.USER`

    Raises
    ------
    CommandIsNotCoroutine
        If the command function is not a coro
    InvalidCommandName
        If the command name does not follow the regex ``^[\\w-]{1,32}$``
    InvalidCommandGuild
        If the guild id is invalid
    CommandDescriptionTooLong
        Descriptions max 100 characters
        If the annotation on an argument is too long (also max 100)
    CommandAlreadyRegistered
        If the command already exists
    InvalidArgumentAnnotation
        Annotation amount is max 25,
        Not a valid argument type,
        Annotations must consist of name and value
    """  # noqa: E501
    return register_command(
        func=func,
        app_command_type=AppCommandType.MESSAGE,
        name=name,
        enable_default=enable_default,
        guild=guild,
        cooldown=cooldown,
        cooldown_scale=cooldown_scale,
        cooldown_scope=cooldown_scope,
    )


def register_command(
    func=None,  # Missing typehint?
    *,
    app_command_type: Optional[AppCommandType] = None,
    name: Optional[str] = None,
    description: Optional[str] = MISSING,
    enable_default: Optional[bool] = True,
    guild: Optional[Union[Snowflake, int, str]] = None,
    cooldown: Optional[int] = 0,
    cooldown_scale: Optional[float] = 60.0,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
    command_options=MISSING,  # Missing typehint?
    parent: Optional[Union[Group, Subgroup]] = MISSING
):
    if func is None:
        return partial(
            register_command,
            name=name,
            app_command_type=app_command_type,
            description=description,
            enable_default=enable_default,
            guild=guild,
            cooldown=cooldown,
            cooldown_scale=cooldown_scale,
            cooldown_scope=cooldown_scope,
            parent=parent
        )

    cmd = name or func.__name__

    if not re.match(REGULAR_COMMAND_NAME_REGEX, cmd):
        raise InvalidCommandName(
            f"Command `{cmd}` doesn't follow the name requirements."
            " Ensure to match the following regex:"
            f" {REGULAR_COMMAND_NAME_REGEX.pattern}"
        )

    if not iscoroutinefunction(func) and not isasyncgenfunction(func):
        raise CommandIsNotCoroutine(
            f"Command with call `{func.__name__}` is not a coroutine, "
            "which is required for commands."
        )

    try:
        guild_id = Snowflake(guild) if guild else MISSING
    except ValueError:
        raise InvalidCommandGuild(
            f"Command with call `{func.__name__}` its `guilds` parameter "
            "contains a non valid guild id."
        )

    if description and len(description) > 100:
        raise CommandDescriptionTooLong(
            f"Command `{cmd}` (`{func.__name__}`) its description exceeds "
            "the 100 character limit."
        )

    group = MISSING
    sub_group = MISSING

    if isinstance(parent, Group):
        group = parent
    if isinstance(parent, Subgroup):
        group = parent.parent
        sub_group = parent

    if reg := ChatCommandHandler.register.get(
        _hash_app_command_params(cmd, guild, app_command_type, group, sub_group)
    ):
        raise CommandAlreadyRegistered(
            f"Command `{cmd}` (`{func.__name__}`) has already been "
            f"registered by `{reg.call.__name__}`."
        )

    ChatCommandHandler.register[
        _hash_app_command_params(cmd, guild_id, app_command_type, group, sub_group)
    ] = ClientCommandStructure(
        call=func,
        cooldown=cooldown,
        cooldown_scale=cooldown_scale,
        cooldown_scope=cooldown_scope,
        group=group,
        sub_group=sub_group,
        app=AppCommand(
            name=cmd,
            description=description,
            type=app_command_type,
            default_permission=enable_default,
            options=command_options,
            guild_id=guild_id
        ),
    )

    _log.info(f"Registered command `{cmd}` to `{func.__name__}` locally.")
    return func


class ChatCommandHandler(metaclass=Singleton):
    """Singleton containing methods used to handle various commands

    The register and built_register
    -------------------------------
    I found the way Discord expects commands to be registered to be very different than
    how you want to think about command registration. i.e. Discord wants nesting but we
    don't want any nesting. Nesting makes it hard to think about commands and also will
    increase lookup time.
    The way this problem is avoided is by storing a version of the commands that we can
    deal with as library developers and a version of the command that Discord thinks we
    should provide. That is where the register and the built_register help simplify the
    design of the library.
    The register is simply where the "Pincer version" of commands gets saved to memory.
    The built_register is where the version of commands that Discord requires is saved.
    The register allows for O(1) lookups by storing commands in a Python dictionary. It
    does cost some memory to save two copies in the current iteration of the system but
    we should be able to drop the built_register in runtime if we want to. I don't feel
    that lost maintainability from this is optimal. We can index by in O(1) by checking
    the register but can still use the built_register if we need to do a nested lookup.

    Attributes
    ----------
    client: :class:`Client`
        The client object
    managers: Dict[:class:`str`, :class:`~typing.Any`]
        Dictionary of managers
    register: Dict[:class:`str`, :class:`~pincer.objects.app.command.ClientCommandStructure`]
        Dictionary of ``ClientCommandStructure``
    built_register: Dict[:class:`str`, :class:`~pincer.objects.app.command.ClientCommandStructure`]
        Dictionary of ``ClientCommandStructure`` where the commands are converted to
        the format that Discord expects for sub commands and sub command groups.
    """  # noqa: E501

    has_been_initialized = False
    managers: Dict[str, Any] = {}
    register: Dict[str, ClientCommandStructure] = {}
    built_register: Dict[str, AppCommand] = {}

    # Endpoints:
    __get = "/commands"
    __delete = "/commands/{command.id}"
    __update = "/commands/{command.id}"
    __add = "/commands"
    __add_guild = "/guilds/{command.guild_id}/commands"
    __get_guild = "/guilds/{guild_id}/commands"
    __update_guild = "/guilds/{command.guild_id}/commands/{command.id}"
    __delete_guild = "/guilds/{command.guild_id}/commands/{command.id}"

    def __init__(self, client: Client):
        self.client = client
        self._api_commands: List[AppCommand] = []
        logging.debug(
            "%i commands registered.", len(ChatCommandHandler.register.items())
        )
        self.client.throttler.throttle = dict(
            map(
                lambda cmd: (cmd.call, {}), ChatCommandHandler.register.values()
            )
        )

        self.__prefix = f"applications/{self.client.bot.id}"

    async def get_commands(self) -> List[AppCommand]:
        """|coro|

        Get a list of app commands from Discord

        Returns
        -------
        List[:class:`~pincer.objects.app.command.AppCommand`]
            List of commands.
        """
        # TODO: Update if discord adds bulk get guild commands
        guild_commands = await gather(
            *map(
                lambda guild: self.client.http.get(
                    self.__prefix
                    + self.__get_guild.format(
                        guild_id=guild.id if isinstance(guild, Guild) else guild
                    )
                ),
                self.client.guilds,
            )
        )
        return list(
            map(
                AppCommand.from_dict,
                await self.client.http.get(self.__prefix + self.__get)
                + [cmd for guild in guild_commands for cmd in guild],
            )
        )

    async def remove_command(self, cmd: AppCommand):
        """|coro|

        Remove a specific command

        Parameters
        ----------
        cmd : :class:`~pincer.objects.app.command.AppCommand`
            What command to delete
        """
        # TODO: Update if discord adds bulk delete commands
        if cmd.guild_id:
            _log.info(
                "Removing command `%s` with guild id %d from Discord",
                cmd.name,
                cmd.guild_id,
            )
        else:
            _log.info("Removing global command `%s` from Discord", cmd.name)

        remove_endpoint = self.__delete_guild if cmd.guild_id else self.__delete

        await self.client.http.delete(
            self.__prefix + remove_endpoint.format(command=cmd)
        )

    async def add_command(self, cmd: AppCommand):
        """|coro|

        Add an app command

        Parameters
        ----------
        cmd : :class:`~pincer.objects.app.command.AppCommand`
            Command to add
        """
        _log.info("Updated or registered command `%s` to Discord", cmd.name)

        add_endpoint = self.__add

        if cmd.guild_id:
            add_endpoint = self.__add_guild.format(command=cmd)

        await self.client.http.post(
            self.__prefix + add_endpoint, data=cmd.to_dict()
        )

    async def add_commands(self, commands: List[AppCommand]):
        """|coro|

        Add a list of app commands

        Parameters
        ----------
        commands : List[:class:`~pincer.objects.app.command.AppCommand`]
            List of command objects to add
        """
        await gather(*map(lambda cmd: self.add_command(cmd), commands))

    @staticmethod
    def __build_local_commands():
        """Builds the commands into the format that Discord expects. See class info
        for the reasoning.
        """
        for cmd in ChatCommandHandler.register.values():

            if cmd.sub_group:
                # If a command has a sub_group, it must be nested 2 levels deep.
                #
                # command
                #     subcommand-group
                #         subcommand
                #
                # The children of the subcommand-group object are being set to include
                # `cmd` If that subcommand-group object does not exist, it will be
                # created here. The same goes for the top-level command.
                #
                # First make sure the command exists. This command will hold the
                # subcommand-group for `cmd`.

                # `key` represents the hash value for the top-level command that will
                # hold the subcommand.
                key = _hash_app_command_params(
                    cmd.group.name,
                    cmd.app.guild_id,
                    AppCommandType.CHAT_INPUT,
                    None,
                    None,
                )

                if key not in ChatCommandHandler.built_register:
                    ChatCommandHandler.built_register[key] = AppCommand(
                        name=cmd.group.name,
                        description=cmd.group.description,
                        type=AppCommandType.CHAT_INPUT,
                        guild_id=cmd.app.guild_id,
                        options=[]
                    )

                # The top-level command now exists. A subcommand group now if placed
                # inside the top-level command. This subcommand group will hold `cmd`.

                children = ChatCommandHandler.built_register[key].options

                sub_command_group = AppCommandOption(
                    name=cmd.sub_group.name,
                    description=cmd.sub_group.description,
                    type=AppCommandOptionType.SUB_COMMAND_GROUP,
                    options=[]
                )

                # This for-else makes sure that sub_command_group will hold a reference
                # to the subcommand group that we want to modify to hold `cmd`

                for cmd_in_children in children:
                    if (
                        cmd_in_children.name == sub_command_group.name
                        and cmd_in_children.description == sub_command_group.description
                        and cmd_in_children.type == sub_command_group.type
                    ):
                        sub_command_group = cmd_in_children
                        break
                else:
                    children.append(sub_command_group)

                sub_command_group.options.append(AppCommandOption(
                    name=cmd.app.name,
                    description=cmd.app.description,
                    type=AppCommandOptionType.SUB_COMMAND,
                    options=cmd.app.options,
                ))

                continue

            if cmd.group:
                # Any command at this point will only have one level of nesting.
                #
                # Command
                #    subcommand
                #
                # A subcommand object is what is being generated here. If there is no
                # top level command, it will be created here.

                # `key` represents the hash value for the top-level command that will
                # hold the subcommand.

                key = _hash_app_command_params(
                    cmd.group.name,
                    cmd.app.guild_id,
                    AppCommandOptionType.SUB_COMMAND,
                    None,
                    None
                )

                if key not in ChatCommandHandler.built_register:
                    ChatCommandHandler.built_register[key] = AppCommand(
                        name=cmd.group.name,
                        description=cmd.group.description,
                        type=AppCommandOptionType.SUB_COMMAND,
                        guild_id=cmd.app.guild_id,
                        options=[]
                    )

                # No checking has to be done before appending `cmd` since it is the
                # lowest level.
                ChatCommandHandler.built_register[key].options.append(
                    AppCommandOption(
                        name=cmd.app.name,
                        description=cmd.app.description,
                        type=AppCommandType.CHAT_INPUT,
                        options=cmd.app.options
                    )
                )

                continue

            # All single-level commands are registered here.
            ChatCommandHandler.built_register[
                _hash_app_command(cmd.app, cmd.group, cmd.sub_group)
            ] = cmd.app

    @staticmethod
    def get_local_registered_commands() -> ValuesView[AppCommand]:
        return ChatCommandHandler.built_register.values()

    async def __get_existing_commands(self):
        """|coro|

        Get AppCommand objects for all commands registered to discord.
        """
        try:
            self._api_commands = await self.get_commands()

        except ForbiddenError:
            logging.error("Cannot retrieve slash commands, skipping...")
            return

    async def __remove_unused_commands(self):
        """|coro|

        Remove commands that are registered by discord but not in use
        by the current client
        """
        local_registered_commands = self.get_local_registered_commands()

        def should_be_removed(target: AppCommand) -> bool:
            for reg_cmd in local_registered_commands:
                # Commands have endpoints based on their `name` amd `guild_id`. Other
                # parameters can be updated instead of deleting and re-registering the
                # command.
                if (
                    target.name == reg_cmd.name
                    and target.guild_id == reg_cmd.guild_id
                ):
                    return False
            return True

        # NOTE: Cannot be generator since it can't be consumed due to lines 743-745
        to_remove = [*filter(should_be_removed, self._api_commands)]

        await gather(
            *map(
                lambda cmd: self.remove_command(cmd),
                to_remove,
            )
        )

        self._api_commands = list(
            filter(lambda cmd: cmd not in to_remove, self._api_commands)
        )

    async def __add_commands(self):
        """|coro|

        Add all new commands which have been registered by the decorator to Discord.

        .. code-block::

            Because commands have unique names within a type and scope, we treat POST
            requests for new commands as upserts. That means making a new command with
            an already-used name for your application will update the existing command.
            `<https://discord.dev/interactions/application-commands#updating-and-deleting-a-command>`_

        Therefore, we don't need to use a separate loop for updating and adding
        commands.
        """
        local_registered_commands = self.get_local_registered_commands()

        def should_be_updated_or_uploaded(target):
            for command in self._api_commands:
                if target == command:
                    return False
            return True

        changed_commands = filter(
            should_be_updated_or_uploaded, local_registered_commands
        )

        for command in changed_commands:
            await self.add_command(command)

    async def initialize(self):
        """|coro|

        Call methods of this class to refresh all app commands
        """
        if ChatCommandHandler.has_been_initialized:
            # Only first shard should be initialized.
            return

        ChatCommandHandler.has_been_initialized = True

        self.__build_local_commands()
        await self.__get_existing_commands()
        await self.__remove_unused_commands()
        await self.__add_commands()


def _hash_app_command(
    command: AppCommand,
    group: Optional[str],
    sub_group: Optional[str]
) -> int:
    """
    See :func:`~pincer.commands.commands._hash_app_command_params` for information.
    """
    return _hash_app_command_params(
        command.name,
        command.guild_id,
        command.type,
        group,
        sub_group
    )


def _hash_app_command_params(
    name: str,
    guild_id: Union[Snowflake, None, MISSING],
    app_command_type: AppCommandType,
    group: Optional[str],
    sub_group: Optional[str]
) -> int:
    """
    The group layout in Pincer is very different from what discord has on their docs.
    You can think of the Pincer group layout like this:

    name: The name of the function that is being called.

    group: The :class:`~pincer.commands.groups.Group` object that this function is
        using.
    sub_option: The :class:`~pincer.commands.groups.Subgroup` object that this
        functions is using.

    Abstracting away this part of the Discord API allows for a much cleaner
    transformation between what users want to input and what commands Discord
    expects.

    Parameters
    ----------
    name : str
        The name of the function for the command
    guild_id : Union[:class:`~pincer.utils.snowflake.Snowflake`, None, MISSING]
        The ID of a guild, None, or MISSING.
    app_command_type : :class:`~pincer.objects.app.command_types.AppCommandType`
        The app command type of the command. NOT THE OPTION TYPE.
    group : str
        The highest level of organization the command is it. This should always be the
        name of the base command. :data:`None` or :data:`MISSING` if not there.
    sub_option : str
        The name of the group that holds the lowest level of options. :data:`None` or
        :data:`MISSING` if not there.
    """
    return hash((name, guild_id, app_command_type, group, sub_group))
