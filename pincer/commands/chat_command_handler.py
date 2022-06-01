# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING

import logging
from asyncio import gather

from ..utils.types import MISSING, Singleton

from ..exceptions import ForbiddenError
from ..objects.guild.guild import Guild
from ..objects.app.command import AppCommand, AppCommandOption
from ..objects.app.command_types import AppCommandOptionType, AppCommandType

if TYPE_CHECKING:
    from typing import List, Dict, Optional, ValuesView, Union
    from .interactable import Interactable
    from ..client import Client
    from ..utils.snowflake import Snowflake
    from ..objects.app.command import InteractableStructure

_log = logging.getLogger(__name__)


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
    register: Dict[:class:`str`, :class:`~pincer.objects.app.command.InteractableStructure`[:class:`~pincer.objects.app.command.AppCommand`]]
        Dictionary of ``InteractableStructure``
    built_register: Dict[:class:`str`, :class:`~pincer.objects.app.command.AppCommand`]]
        Dictionary of ``InteractableStructure`` where the commands are converted to
        the format that Discord expects for sub commands and sub command groups.
    """  # noqa: E501

    has_been_initialized = False
    managers: List[Interactable] = []
    register: Dict[str, InteractableStructure[AppCommand]] = {}
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
        _log.debug("%i commands registered.", len(ChatCommandHandler.register))

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
            *(
                self.client.http.get(
                    self.__prefix
                    + self.__get_guild.format(
                        guild_id=guild.id if isinstance(guild, Guild) else guild
                    )
                )
                for guild in self.client.guilds
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
        await gather(*map(self.add_command, commands))

    @staticmethod
    def __build_local_commands():
        """Builds the commands into the format that Discord expects. See class info
        for the reasoning.
        """

        # Reset the built register
        ChatCommandHandler.built_register = {}

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
                    cmd.metadata.guild_id,
                    AppCommandType.CHAT_INPUT,
                    None,
                    None,
                )

                if key not in ChatCommandHandler.built_register:
                    ChatCommandHandler.built_register[key] = AppCommand(
                        name=cmd.group.name,
                        description=cmd.group.description,
                        type=AppCommandType.CHAT_INPUT,
                        guild_id=cmd.metadata.guild_id,
                        options=[],
                    )

                # The top-level command now exists. A subcommand group now if placed
                # inside the top-level command. This subcommand group will hold `cmd`.

                children = ChatCommandHandler.built_register[key].options

                sub_command_group = AppCommandOption(
                    name=cmd.sub_group.name,
                    description=cmd.sub_group.description,
                    type=AppCommandOptionType.SUB_COMMAND_GROUP,
                    options=[],
                )

                # This for-else makes sure that sub_command_group will hold a reference
                # to the subcommand group that we want to modify to hold `cmd`

                for cmd_in_children in children:
                    if (
                        cmd_in_children.name == sub_command_group.name
                        and cmd_in_children.description
                        == sub_command_group.description
                        and cmd_in_children.type == sub_command_group.type
                    ):
                        sub_command_group = cmd_in_children
                        break
                else:
                    children.append(sub_command_group)

                sub_command_group.options.append(
                    AppCommandOption(
                        name=cmd.metadata.name,
                        description=cmd.metadata.description,
                        type=AppCommandOptionType.SUB_COMMAND,
                        options=cmd.metadata.options,
                    )
                )

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
                    cmd.metadata.guild_id,
                    AppCommandOptionType.SUB_COMMAND,
                    None,
                    None,
                )

                if key not in ChatCommandHandler.built_register:
                    ChatCommandHandler.built_register[key] = AppCommand(
                        name=cmd.group.name,
                        description=cmd.group.description,
                        type=AppCommandOptionType.SUB_COMMAND,
                        guild_id=cmd.metadata.guild_id,
                        options=[],
                    )

                # No checking has to be done before appending `cmd` since it is the
                # lowest level.
                ChatCommandHandler.built_register[key].options.append(
                    AppCommandOption(
                        name=cmd.metadata.name,
                        description=cmd.metadata.description,
                        type=AppCommandType.CHAT_INPUT,
                        options=cmd.metadata.options,
                    )
                )

                continue

            # All single-level commands are registered here.
            ChatCommandHandler.built_register[
                _hash_interactable_structure(cmd)
            ] = cmd.metadata

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
            # Commands have endpoints based on their `name` amd `guild_id`. Other
            # parameters can be updated instead of deleting and re-registering the
            # command.
            return all(
                target.name != reg_cmd.name
                and target.guild_id != reg_cmd.guild_id
                for reg_cmd in local_registered_commands
            )

        # NOTE: Cannot be generator since it can't be consumed due to lines 743-745
        to_remove = [*filter(should_be_removed, self._api_commands)]

        await gather(*(self.remove_command(cmd) for cmd in to_remove))

        self._api_commands = [
            cmd for cmd in self._api_commands if cmd not in to_remove
        ]

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
        for command in self.get_local_registered_commands():
            if command not in self._api_commands:
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


def _hash_interactable_structure(
    interactable: InteractableStructure[AppCommand],
):
    return _hash_app_command(
        interactable.metadata, interactable.group, interactable.sub_group
    )


def _hash_app_command(
    command: AppCommand, group: Optional[str], sub_group: Optional[str]
) -> int:
    """
    See :func:`~pincer.commands.commands._hash_app_command_params` for information.
    """
    return _hash_app_command_params(
        command.name, command.guild_id, command.type, group, sub_group
    )


def _hash_app_command_params(
    name: str,
    guild_id: Union[Snowflake, None, MISSING],
    app_command_type: AppCommandType,
    group: Optional[str],
    sub_group: Optional[str],
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
