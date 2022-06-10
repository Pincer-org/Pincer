# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
import re
from asyncio import iscoroutinefunction
from functools import partial
from inspect import Signature, isasyncgenfunction, _empty
from typing import TYPE_CHECKING, Any, Callable, TypeVar, Union, List

from . import __package__
from .chat_command_handler import ChatCommandHandler, _hash_app_command_params
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
from ..utils.types import APINullable, MISSING
from ..exceptions import (
    CommandIsNotCoroutine,
    CommandAlreadyRegistered,
    TooManyArguments,
    InvalidArgumentAnnotation,
    CommandDescriptionTooLong,
    InvalidCommandGuild,
    InvalidCommandName,
)
from ..objects import (
    ThrottleScope,
    AppCommand,
    Role,
    User,
    Channel,
    Mentionable,
    MessageContext,
)
from ..objects.app import (
    AppCommandOptionType,
    AppCommandOption,
    InteractableStructure,
    AppCommandType,
)
from ..utils import should_pass_ctx
from ..utils.signature import get_signature_and_params

if TYPE_CHECKING:
    from typing import Optional

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
    parent: Optional[Union[Group, Subgroup]] = None,
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
            parent=parent,
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

        # check if None to keep the type checker happy that its Any
        if argument_type is not None and hasattr(argument_type, "__args__"):
            # this is a Union, hopefully an Optional/Union[T, None]
            # Optional[T] is an alias to Union[T, None]
            args = argument_type.__args__

            if len(args) != 2 or args[1] != type(None):
                raise InvalidArgumentAnnotation(
                    "`Union` is not a supported option type"
                )

            argument_type = args[0]

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

        argument_description = get_arg(Description) or "Description not set"

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
                if isinstance(choice.value, int) and argument_type is float:
                    continue
                if not isinstance(choice.value, argument_type):
                    raise InvalidArgumentAnnotation(
                        "Choice value must match the command type"
                    )

        channel_types = get_arg(ChannelTypes)
        if channel_types is not MISSING and argument_type is not Channel:
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
        parent=parent,
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
    if func is None:
        return partial(
            user_command,
            name=name,
            enable_default=enable_default,
            guild=guild,
            cooldown=cooldown,
            cooldown_scale=cooldown_scale,
            cooldown_scope=cooldown_scope,
        )

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
    if func is None:
        return partial(
            message_command,
            name=name,
            enable_default=enable_default,
            guild=guild,
            cooldown=cooldown,
            cooldown_scale=cooldown_scale,
            cooldown_scope=cooldown_scope,
        )

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
    func: Callable[..., Any] = None,
    app_command_type: Optional[AppCommandType] = None,
    name: Optional[str] = None,
    description: Optional[str] = MISSING,
    enable_default: Optional[bool] = True,
    guild: Optional[Union[Snowflake, int, str]] = None,
    cooldown: Optional[int] = 0,
    cooldown_scale: Optional[float] = 60.0,
    cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER,
    command_options=MISSING,  # Missing typehint?
    parent: Optional[Union[Group, Subgroup]] = MISSING,
):
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

    _log.info(f"Registered command `{cmd}` to `{func.__name__}` locally.")

    interactable = InteractableStructure(
        call=func,
        cooldown=cooldown,
        cooldown_scale=cooldown_scale,
        cooldown_scope=cooldown_scope,
        manager=None,
        group=group,
        sub_group=sub_group,
        metadata=AppCommand(
            name=cmd,
            description=description,
            type=app_command_type,
            default_permission=enable_default,
            options=command_options,
            guild_id=guild_id,
        ),
    )

    ChatCommandHandler.register[
        _hash_app_command_params(
            cmd, guild_id, app_command_type, group, sub_group
        )
    ] = interactable

    return interactable
