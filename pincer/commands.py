# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import annotations

import logging
from asyncio import iscoroutinefunction
from inspect import Signature
from typing import Optional, Dict, List, Any, Tuple, get_origin, get_args, Union

from . import __package__
from .exceptions import (
    CommandIsNotCoroutine, CommandAlreadyRegistered, TooManyArguments,
    InvalidArgumentAnnotation, CommandDescriptionTooLong, InvalidCommandGuild
)
from .objects.app_command import (
    AppCommand, AppCommandType, ClientCommandStructure,
    AppCommandOption, AppCommandOptionType
)
from .utils import (
    get_signature_and_params, get_index, should_pass_ctx, Coro, Snowflake,
    MISSING
)

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
        guild: Union[Snowflake, int, str] = None
):
    # TODO: Fix docs
    def decorator(func: Coro):
        if not iscoroutinefunction(func):
            raise CommandIsNotCoroutine(
                f"Command with call `{func.__name__}` is not a coroutine, "
                "which is required for commands."
            )

        cmd = name or func.__name__

        # TODO: Perform name check on cmd with r"^[\w-]{1,32}$"

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

        for param in params:
            annotation, required = sig[param].annotation, True

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

            param_type = _options_type_link.get(annotation)
            if not param_type:
                raise InvalidArgumentAnnotation(
                    f"Annotation `{annotation}` on parameter "
                    f"`{param}` in command `{cmd}` (`{func.__name__}`) is not "
                    f"a valid type."
                )

            options.append(
                AppCommandOption(
                    type=param_type,
                    name=param,
                    description=description,
                    required=required
                )
            )

        ChatCommandHandler.register[cmd] = ClientCommandStructure(
            call=func,
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
            f"%i commands registered.",
            len(ChatCommandHandler.register.items())
        )

    async def __init_existing_commands(self):
        # TODO: Fix docs
        async with self.client.http as http:
            res = await http.get(f"applications/{self.client.bot.id}/commands")
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

        async with self.client.http as http:
            for cmd in to_remove:
                await http.delete(
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

            if (
                api.options is not MISSING
                and list(
                    map(AppCommandOption.from_dict, options)
                ) != api.options
            ):
                update["options"] = options

            return update

        for idx, api_cmd in enumerate(self._api_commands):
            for loc_cmd in ChatCommandHandler.register.values():
                if api_cmd.name != loc_cmd.app.name:
                    continue

                changes = get_changes(api_cmd, loc_cmd.app)

                if changes:
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

        async with self.client.http as http:
            for cmd_id, changes in to_update.items():
                await http.patch(
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
            async with self.client.http as http:
                endpoint = f"applications/{self.client.bot.id}"
                for cmd in commands_to_add:
                    if cmd.app.guild_id is not MISSING:
                        endpoint += f"/guilds/{cmd.app.guild_id}"

                    await http.post(
                        endpoint + "/commands",
                        cmd.app.to_dict()
                    )

    async def initialize(self):
        # TODO: Fix docs
        await self.__init_existing_commands()
        await self.__remove_unused_commands()
        await self.__update_existing_commands()
        await self.__add_commands()
