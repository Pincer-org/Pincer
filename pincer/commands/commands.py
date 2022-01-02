# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
import re
from asyncio import iscoroutinefunction, gather
from functools import partial
from inspect import Signature, isasyncgenfunction, _empty
from typing import TYPE_CHECKING, Union, List

from . import __package__
from ..commands.arg_types import (
    ChannelTypes,
    CommandArg,
    Description,
    Choices,
    MaxValue,
    MinValue,
)
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
from ..utils import get_index, should_pass_ctx
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


def command(
    func=None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = "Description not set",
    enable_default: Optional[bool] = True,
    guild: Union[Snowflake, int, str] = None,
    cooldown: Optional[int] = 0,
    cooldown_scale: Optional[float] = 60,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
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
                    Description["Do something cool"],
                    Choices[Choice["first value", 1], 5]
                ],
                optional_int: CommandArg[
                    int,
                    MinValue[10],
                    MaxValue[100],
                ] = 50
            ):
                return Message(
                    f"You chose {amount}, {name}, {letter}",
                    flags=InteractionFlags.EPHEMERAL
                )


    References from above:
        :class:`~client.Client`,
        :class:`~objects.message.message.Message`,
        :class:`~objects.message.context.MessageContext`,
        :class:`~pincer.objects.app.interaction_flags.InteractionFlags`,
        :class:`~pincer.commands.arg_types.Choices`,
        :class:`~pincer.commands.arg_types.Choice`,
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

        if type(annotation) is not CommandArg:
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
                "Type must be CommandArg or other valid type"
            )

        command_type = _options_type_link[annotation.command_type]
        argument_description = (
            annotation.get_arg(Description) or "Description not set"
        )
        choices = annotation.get_arg(Choices)

        if choices is not MISSING and annotation.command_type not in {
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
                    and annotation.command_type is float
                ):
                    continue
                if not isinstance(choice.value, annotation.command_type):
                    raise InvalidArgumentAnnotation(
                        "Choice value must match the command type"
                    )

        channel_types = annotation.get_arg(ChannelTypes)
        if (
            channel_types is not MISSING
            and annotation.command_type is not Channel
        ):
            raise InvalidArgumentAnnotation(
                "ChannelTypes are only available for Channels"
            )

        max_value = annotation.get_arg(MaxValue)
        min_value = annotation.get_arg(MinValue)

        for i, value in enumerate((min_value, max_value)):
            if (
                value is not MISSING
                and annotation.command_type is not int
                and annotation.command_type is not float
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
    """
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
    cooldown_scale: Optional[float] = 60,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
    command_options=MISSING,  # Missing typehint?
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

    if reg := ChatCommandHandler.register.get(
        hash_app_command_params(cmd, guild, app_command_type)
    ):
        raise CommandAlreadyRegistered(
            f"Command `{cmd}` (`{func.__name__}`) has already been "
            f"registered by `{reg.call.__name__}`."
        )

    ChatCommandHandler.register[
        hash_app_command_params(cmd, guild_id, app_command_type)
    ] = ClientCommandStructure(
        call=func,
        cooldown=cooldown,
        cooldown_scale=cooldown_scale,
        cooldown_scope=cooldown_scope,
        app=AppCommand(
            name=cmd,
            description=description,
            type=app_command_type,
            default_permission=enable_default,
            options=command_options,
            guild_id=guild_id,
        ),
    )

    _log.info(f"Registered command `{cmd}` to `{func.__name__}` locally.")
    return func


class ChatCommandHandler(metaclass=Singleton):
    """Metaclass containing methods used to handle various commands

    Attributes
    ----------
    client: :class:`Client`
        The client object
    managers: Dict[:class:`str`, :class:`~typing.Any`]
        Dictionary of managers
    register: Dict[:class:`str`, :class:`~objects.app.command.ClientCommandStructure`]
        Dictionary of ``ClientCommandStructure``
    """

    has_been_initialized = False
    managers: Dict[str, Any] = {}
    register: Dict[str, ClientCommandStructure] = {}

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

        Get a list of app commands

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

        ChatCommandHandler.register.pop(hash_app_command(cmd), None)

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

        res = await self.client.http.post(
            self.__prefix + add_endpoint, data=cmd.to_dict()
        )

        ChatCommandHandler.register[hash_app_command(cmd)].app.id = Snowflake(
            res["id"]
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

    async def __get_existing_commands(self):
        """|coro|

        Get AppCommand objects for all commands registered to discord.
        """
        try:
            self._api_commands = await self.get_commands()

        except ForbiddenError:
            logging.error("Cannot retrieve slash commands, skipping...")
            return

        for api_cmd in self._api_commands:
            cmd = ChatCommandHandler.register.get(hash_app_command(api_cmd))
            if cmd and cmd.app == api_cmd:
                cmd.app = api_cmd

    async def __remove_unused_commands(self):
        """|coro|

        Remove commands that are registered by discord but not in use
        by the current client
        """
        local_registered_commands = [
            registered_cmd.app for registered_cmd
            in ChatCommandHandler.register.values()
        ]

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
        to_remove = list(filter(should_be_removed, self._api_commands))

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
        local_registered_commands = [
            registered_cmd.app for registered_cmd
            in ChatCommandHandler.register.values()
        ]

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
        await self.__get_existing_commands()
        await self.__remove_unused_commands()
        await self.__add_commands()


def hash_app_command(command: AppCommand) -> int:
    return hash_app_command_params(command.name, command.guild_id, command.type)


def hash_app_command_params(
    name: str, guild_id: Snowflake, app_command_type: AppCommandType
) -> int:
    return hash((name, guild_id, app_command_type))
