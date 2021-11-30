# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
import re
from asyncio import iscoroutinefunction, gather
from copy import deepcopy
from functools import partial
from inspect import Signature, isasyncgenfunction, _empty
from typing import TYPE_CHECKING, Union, Tuple, List

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

COMMAND_NAME_REGEX = re.compile(r"^[\w-]{1,32}$")

_log = logging.getLogger(__package__)

_options_type_link = {
    # TODO: Implement other types:
    Signature.empty: AppCommandOptionType.STRING,
    str: AppCommandOptionType.STRING,
    int: AppCommandOptionType.INTEGER,
    bool: AppCommandOptionType.BOOLEAN,
    float: AppCommandOptionType.NUMBER,
    User: AppCommandOptionType.USER,
    Channel: AppCommandOptionType.CHANNEL,
    Role: AppCommandOptionType.ROLE,
    Mentionable: AppCommandOptionType.MENTIONABLE
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
    """
    # noqa: E501
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
                     # This bot doesn't like being DMed so it won't respond
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
    """
    # noqa: E501
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

    if not iscoroutinefunction(func) and not isasyncgenfunction(func):
        raise CommandIsNotCoroutine(
            f"Command with call `{func.__name__}` is not a coroutine, "
            "which is required for commands."
        )

    cmd = name or func.__name__

    if not re.match(COMMAND_NAME_REGEX, cmd):
        raise InvalidCommandName(
            f"Command `{cmd}` doesn't follow the name requirements."
            " Ensure to match the following regex:"
            f" {COMMAND_NAME_REGEX.pattern}"
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

    if reg := ChatCommandHandler.register.get(cmd):
        raise CommandAlreadyRegistered(
            f"Command `{cmd}` (`{func.__name__}`) has already been "
            f"registered by `{reg.call.__name__}`."
        )

    ChatCommandHandler.register[cmd] = ClientCommandStructure(
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

    _log.info(f"Registered command `{cmd}` to `{func.__name__}`.")
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

    async def remove_command(self, cmd: AppCommand, keep=False):
        """|coro|

        Remove a specific command

        Parameters
        ----------
        cmd : :class:`~pincer.objects.app.command.AppCommand`
            What command to delete
        keep : bool
            Whether the command should be removed from the ChatCommandHandler.
            Set to :data:`True` to keep the command.
            |default| :data:`False`
        """
        # TODO: Update if discord adds bulk delete commands
        remove_endpoint = self.__delete_guild if cmd.guild_id else self.__delete

        await self.client.http.delete(
            self.__prefix + remove_endpoint.format(command=cmd)
        )

        if not keep and ChatCommandHandler.register.get(cmd.name):
            del ChatCommandHandler.register[cmd.name]

    async def remove_commands(
        self, commands: List[AppCommand], /, keep: List[AppCommand] = None
    ):
        """|coro|

        Remove a list of commands

        Parameters
        ----------
        commands : List[:class:`~pincer.objects.app.command.AppCommand`]
            List of commands to delete
        keep: List[:class:`~pincer.objects.app.command.AppCommand`]
            List of commands that should not be removed from the
            ChatCommandHandler.
            |default| :data:`None`
        """
        await gather(
            *list(
                map(
                    lambda cmd: self.remove_command(cmd, cmd in (keep or [])),
                    commands,
                )
            )
        )

    async def update_command(self, cmd: AppCommand, changes: Dict[str, Any]):
        """|coro|

        Update a command with changes

        Parameters
        ----------
        cmd : :class:`~objects.app.command.AppCommand`
            What command to update
        changes : Dict[:class:`str`, Any]
            Dictionary of changes
        """
        # TODO: Update if discord adds bulk update commands
        update_endpoint = self.__update_guild if cmd.guild_id else self.__update

        await self.client.http.patch(
            self.__prefix + update_endpoint.format(command=cmd), data=changes
        )

        for key, value in changes.items():
            setattr(ChatCommandHandler.register[cmd.name], key, value)

    async def update_commands(
        self, to_update: Dict[AppCommand, Dict[str, Any]]
    ):
        """|coro|

        Update a list of app commands with changes

        Parameters
        ----------
        to_update : Dict[:class:`~objects.app.command.AppCommand`, Dict[:class:`str`, Any]]
            Dictionary of commands to changes where changes is a dictionary too
        """
        # noqa: E501
        await gather(
            *list(
                map(
                    lambda cmd: self.update_command(cmd[0], cmd[1]),
                    to_update.items(),
                )
            )
        )

    async def add_command(self, cmd: AppCommand):
        """|coro|

        Add an app command

        Parameters
        ----------
        cmd : :class:`~pincer.objects.app.command.AppCommand`
            Command to add
        """
        add_endpoint = self.__add

        if cmd.guild_id:
            add_endpoint = self.__add_guild.format(command=cmd)

        res = await self.client.http.post(
            self.__prefix + add_endpoint, data=cmd.to_dict()
        )

        ChatCommandHandler.register[cmd.name].app.id = Snowflake(res["id"])

    async def add_commands(self, commands: List[AppCommand]):
        """|coro|

        Add a list of app commands

        Parameters
        ----------
        commands : List[:class:`~pincer.objects.app.command.AppCommand`]
            List of command objects to add
        """
        await gather(*list(map(lambda cmd: self.add_command(cmd), commands)))

    async def __init_existing_commands(self):
        """|coro|

        Initiate existing commands
        """
        try:
            self._api_commands = await self.get_commands()

        except ForbiddenError:
            logging.error("Cannot retrieve slash commands, skipping...")

            return

        for api_cmd in self._api_commands:
            cmd = ChatCommandHandler.register.get(api_cmd.name)
            if cmd and cmd.app == api_cmd:
                cmd.app = api_cmd

    async def __remove_unused_commands(self):
        """|coro|

        Remove commands that are registered by discord but not in use
        by the current client
        """
        registered_commands = list(
            map(
                lambda registered_cmd: registered_cmd.app,
                ChatCommandHandler.register.values(),
            )
        )
        keep = []

        def predicate(target: AppCommand) -> bool:
            for reg_cmd in registered_commands:
                reg_cmd: AppCommand = reg_cmd
                if target == reg_cmd:
                    return False
                elif target.name == reg_cmd.name:
                    keep.append(target)
            return True

        to_remove = list(filter(predicate, self._api_commands))

        await self.remove_commands(to_remove, keep=keep)

        self._api_commands = list(
            filter(lambda cmd: cmd not in to_remove, self._api_commands)
        )

    async def __update_existing_commands(self):
        """|coro|

        Update all commands where its structure doesn't match the
        structure that discord has registered.
        """
        to_update: Dict[AppCommand, Dict[str, Any]] = {}

        def get_changes(api: AppCommand, local: AppCommand) -> Dict[str, Any]:
            update: Dict[str, Any] = {}

            if api.description != local.description:
                update["description"] = local.description

            if api.default_permission != local.default_permission:
                update["default_permission"] = local.default_permission

            options: List[Dict[str, Any]] = []
            if api.options is not MISSING:
                if len(api.options) == len(local.options):

                    def get_option(
                        args: Tuple[int, Any]
                    ) -> Optional[Dict[str, Any]]:
                        index, api_option = args

                        if opt := get_index(local.options, index):
                            return opt.to_dict()

                    options = list(
                        filter(
                            lambda opt: opt is not None,
                            map(get_option, enumerate(api.options)),
                        )
                    )
                else:
                    options = local.options

            if (
                api.options is not MISSING
                and list(map(AppCommandOption.from_dict, options))
                != api.options
            ):
                update["options"] = options

            return update

        for idx, api_cmd in enumerate(self._api_commands):
            for loc_cmd in ChatCommandHandler.register.values():
                if api_cmd.name != loc_cmd.app.name:
                    continue

                changes = get_changes(api_cmd, loc_cmd.app)

                if not changes:
                    continue

                api_update = []
                if changes.get("options"):
                    for option in changes["options"]:
                        api_update.append(
                            option.to_dict()
                            if isinstance(option, AppCommandOption)
                            else option
                        )

                to_update[api_cmd] = {"options": api_update}

                for key, change in changes.items():
                    if key == "options":
                        self._api_commands[idx].options = list(
                            map(AppCommandOption.from_dict, change)
                        )
                    else:
                        setattr(self._api_commands[idx], key, change)

        await self.update_commands(to_update)

    async def __add_commands(self):
        """|coro|

        Add all new commands which have been registered by the decorator
        to Discord
        """
        to_add = deepcopy(ChatCommandHandler.register)
        for reg_cmd in self._api_commands:
            try:
                del to_add[reg_cmd.name]
            except IndexError:
                pass

        await self.add_commands(list(map(lambda cmd: cmd.app, to_add.values())))

    async def initialize(self):
        """|coro|

        Call methods of this class to refresh all app commands
        """
        await self.__init_existing_commands()
        await self.__remove_unused_commands()
        await self.__update_existing_commands()
        await self.__add_commands()
