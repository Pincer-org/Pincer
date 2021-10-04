# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
import re
from asyncio import iscoroutinefunction
from inspect import Signature, isasyncgenfunction
from typing import Optional, Dict, List, Any, Tuple, get_origin, get_args, Union

from . import __package__
from .exceptions import (
    CommandIsNotCoroutine, CommandAlreadyRegistered, TooManyArguments,
    InvalidArgumentAnnotation, CommandDescriptionTooLong, InvalidCommandGuild,
    InvalidCommandName
)
from .objects import ThrottleScope, AppCommand
from .objects.app import (
    AppCommandOptionType, AppCommandOption, AppCommandOptionChoice,
    ClientCommandStructure, AppCommandType
)
from .utils import (
    get_signature_and_params, get_index, should_pass_ctx, Coro, Snowflake,
    MISSING, choice_value_types, Choices
)

COMMAND_NAME_REGEX = re.compile(r"^[\w-]{1,32}$")

_log = logging.getLogger(__package__)

_options_type_link = {
    # TODO: Implement other types:
    Signature.empty: AppCommandOptionType.STRING,
    str: AppCommandOptionType.STRING,
    int: AppCommandOptionType.INTEGER,
    bool: AppCommandOptionType.BOOLEAN,
    float: AppCommandOptionType.NUMBER
}


def command(
        name: Optional[str] = None,
        description: Optional[str] = "Description not set",
        enable_default: Optional[bool] = True,
        guild: Union[Snowflake, int, str] = None,
        cooldown: Optional[int] = 0,
        cooldown_scale: Optional[float] = 60,
        cooldown_scope: Optional[ThrottleScope] = ThrottleScope.USER
):
    # TODO: Fix docs
    # TODO: Fix docs w guild
    # TODO: Fix docs w cooldown
    # TODO: Fix docs w context
    # TODO: Fix docs w argument descriptions
    # TODO: Fix docs w argument choices
    def decorator(func: Coro):
        if not iscoroutinefunction(func) and not isasyncgenfunction(func):
            raise CommandIsNotCoroutine(
                f"Command with call `{func.__name__}` is not a coroutine, "
                "which is required for commands."
            )

        cmd = name or func.__name__

        if not re.match(COMMAND_NAME_REGEX, cmd):
            raise InvalidCommandName(
                f"Command `{cmd}` doesn't follow the name requirements."
                "Ensure to match the following regex:"
                f" {COMMAND_NAME_REGEX.pattern}"
            )

        try:
            guild_id = int(guild) if guild else MISSING
        except ValueError:
            raise InvalidCommandGuild(
                f"Command with call `{func.__name__}` its `guilds` parameter "
                "contains a non valid guild id."
            )

        if len(description) > 100:
            raise CommandDescriptionTooLong(
                f"Command `{cmd}` (`{func.__name__}`) its description exceeds "
                "the 100 character limit."
            )

        if reg := ChatCommandHandler.register.get(cmd):
            raise CommandAlreadyRegistered(
                f"Command `{cmd}` (`{func.__name__}`) has already been "
                f"registered by `{reg.call.__name__}`."
            )

        sig, params = get_signature_and_params(func)
        pass_context = should_pass_ctx(sig, params)

        if len(params) > (25 + pass_context):
            raise TooManyArguments(
                f"Command `{cmd}` (`{func.__name__}`) can only have 25 "
                f"arguments (excluding the context and self) yet {len(params)} "
                "were provided!"
            )

        options: List[AppCommandOption] = []

        for idx, param in enumerate(params):
            if idx == 0 and pass_context:
                continue

            annotation, required = sig[param].annotation, True
            argument_description: Optional[str] = None
            choices: List[AppCommandOptionChoice] = []

            if isinstance(annotation, tuple):
                if len(annotation) != 2:
                    raise InvalidArgumentAnnotation(
                        f"Tuple annotation `{annotation}` on parameter "
                        f"`{param}` in command `{cmd}` (`{func.__name__}`) "
                        "does not consist of two elements. Please follow the "
                        "correct format where the first element is the type"
                        " and the second element is the description."
                    )
                annotation, argument_description = annotation

                if len(argument_description) > 100:
                    raise CommandDescriptionTooLong(
                        f"Tuple annotation `{annotation}` on parameter "
                        f"`{param}` in command `{cmd}` (`{func.__name__}`), "
                        "argument description too long. (maximum length is 100 "
                        "characters)"
                    )

            if get_origin(annotation) is Union:
                args = get_args(annotation)
                if type(None) in args:
                    required = False

                # Do NOT use isinstance as this is a comparison between
                # two values of the type type and isinstance does NOT
                # work here.
                union_args = [t for t in args if t is not type(None)]

                annotation = (
                    get_index(union_args, 0)
                    if len(union_args) == 1
                    else Union[Tuple[List]]
                )

            if get_origin(annotation) is Choices:
                args = get_args(annotation)

                if len(args) > 25:
                    raise InvalidArgumentAnnotation(
                        f"Choices/Literal annotation `{annotation}` on "
                        f"parameter `{param}` in command `{cmd}` "
                        f"(`{func.__name__}`) amount exceeds limit of 25 items!"
                    )

                choice_type = type(args[0])

                for choice in args:
                    choice_name = choice

                    if isinstance(choice, tuple):
                        if len(choice) != 2:
                            raise InvalidArgumentAnnotation(
                                f"Choices/Literal annotation `{annotation}` on "
                                f"parameter `{param}` in command `{cmd}` "
                                f"(`{func.__name__}`), specific choice "
                                "declaration through tuple's must consist of "
                                "2 items. First value is the name and the "
                                "second value is the value."
                            )

                        choice_name, choice = str(choice[0]), choice[1]

                        if choice_type is tuple:
                            choice_type = type(choice)

                    if type(choice) not in choice_value_types:
                        # Properly get all the names of the types
                        valid_types = list(map(
                            lambda x: x.__name__,
                            choice_value_types
                        ))
                        raise InvalidArgumentAnnotation(
                            f"Choices/Literal annotation `{annotation}` on "
                            f"parameter `{param}` in command `{cmd}` "
                            f"(`{func.__name__}`), invalid type received. "
                            "Value must be a member of "
                            f"{', '.join(valid_types)} but "
                            f"{type(choice).__name__} was given!"
                        )
                    elif not isinstance(choice, choice_type):
                        raise InvalidArgumentAnnotation(
                            f"Choices/Literal annotation `{annotation}` on "
                            f"parameter `{param}` in command `{cmd}` "
                            f"(`{func.__name__}`), all values must be of the "
                            "same type!"
                        )

                    choices.append(AppCommandOptionChoice(
                        name=choice_name,
                        value=choice
                    ))

                annotation = choice_type

            param_type = _options_type_link.get(annotation)
            if not param_type:
                raise InvalidArgumentAnnotation(
                    f"Annotation `{annotation}` on parameter "
                    f"`{param}` in command `{cmd}` (`{func.__name__}`) is not "
                    "a valid type."
                )

            options.append(
                AppCommandOption(
                    type=param_type,
                    name=param,
                    description=argument_description or "Description not set",
                    required=required,
                    choices=choices or MISSING
                )
            )

        ChatCommandHandler.register[cmd] = ClientCommandStructure(
            call=func,
            cooldown=cooldown,
            cooldown_scale=cooldown_scale,
            cooldown_scope=cooldown_scope,
            app=AppCommand(
                name=cmd,
                description=description,
                type=AppCommandType.CHAT_INPUT,
                default_permission=enable_default,
                options=options,
                guild_id=guild_id
            )
        )

        _log.info(f"Registered command `{cmd}` to `{func.__name__}`.")

    return decorator


class ChatCommandHandler:
    register: Dict[str, ClientCommandStructure] = {}

    # TODO: Fix docs
    def __init__(self, client):
        # TODO: Fix docs
        self.client = client
        self._api_commands: List[AppCommand] = list()
        logging.debug(
            "%i commands registered.",
            len(ChatCommandHandler.register.items())
        )
        self.client.throttler.throttle = {
            cmd.call: {} for cmd in ChatCommandHandler.register.values()
        }

    async def __init_existing_commands(self):
        # TODO: Fix docs
        res = await self.client.http.get(
            f"applications/{self.client.bot.id}/commands")
        self._api_commands = list(map(AppCommand.from_dict, res))

    async def __remove_unused_commands(self):
        # TODO: Fix docs
        to_remove: List[AppCommand] = list()

        for api_cmd in self._api_commands:
            doesnt_exist = all(
                api_cmd.name != loc_cmd.app.name
                for loc_cmd in ChatCommandHandler.register.values()
            )

            if doesnt_exist:
                to_remove.append(api_cmd)

        for cmd in to_remove:
            await self.client.http.delete(
                f"applications/{self.client.bot.id}/commands/{cmd.id}"
            )

        self._api_commands = [
            cmd for cmd in self._api_commands if cmd not in to_remove
        ]

    async def __update_existing_commands(self):
        # TODO: Fix docs
        to_update: Dict[Snowflake, Dict[str, Any]] = {}

        def get_changes(
                api: AppCommand,
                local: AppCommand
        ) -> Dict[str, Any]:
            update: Dict[str, Any] = {}

            if api.description != local.description:
                update["description"] = local.description

            if api.default_permission != local.default_permission:
                update["default_permission"] = local.default_permission

            options: List[Dict[str, Any]] = []
            if api.options is not MISSING:
                if len(api.options) == len(local.options):
                    for index, api_option in enumerate(api.options):
                        opt: Optional[AppCommandOption] = \
                            get_index(local.options, index)

                        if opt:
                            options.append(opt.to_dict())
                else:
                    options = local.options

            if api.options is not MISSING and list(
                    map(AppCommandOption.from_dict, options)) != api.options:
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

                to_update[api_cmd.id] = {"options": api_update}

                for key, change in changes.items():
                    if key == "options":
                        self._api_commands[idx].options = [
                            AppCommandOption.from_dict(option)
                            for option in change
                        ]
                    else:
                        setattr(self._api_commands[idx], key, change)

        for cmd_id, changes in to_update.items():
            await self.client.http.patch(
                f"applications/{self.client.bot.id}/commands/{cmd_id}",
                changes
            )

    async def __add_commands(self):
        # TODO: Fix docs
        commands_to_add: List[ClientCommandStructure] = [
            cmd for cmd in ChatCommandHandler.register.values()
            if cmd.app not in self._api_commands
        ]

        if commands_to_add:
            for cmd in commands_to_add:
                endpoint = f"applications/{self.client.bot.id}"

                if cmd.app.guild_id is not MISSING:
                    endpoint += f"/guilds/{cmd.app.guild_id}"

                await self.client.http.post(
                    endpoint + "/commands",
                    cmd.app.to_dict()
                )

    async def initialize(self):
        # TODO: Fix docs
        await self.__init_existing_commands()
        await self.__remove_unused_commands()
        await self.__update_existing_commands()
        await self.__add_commands()
