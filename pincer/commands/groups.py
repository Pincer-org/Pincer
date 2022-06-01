# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional


@dataclass
class Group:
    """
    The group object represents a group that commands can be in. This is always a top
    level command.

    .. code-block:: python

        class Bot:

            group = Group("cool_commands")

            @command(parent=group)
            async def a_very_cool_command():
                pass

    This code creates a command called ``cool_commands`` with the subcommand
    ``a_very_cool_command``

    Parameters
    ----------
    name : str
        The name of the command group.
    description : Optional[:class:`str`]
        The description of the command. This has to be sent to Discord, but it does
        nothing, so it is optional.
    """

    name: str
    description: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Subgroup:
    """
    A subgroup of commands. This allows you to create subcommands inside a
    subcommand-group.

    .. code-block:: python

        class Bot:

            group = Group("cool_commands")
            sub_group = Subgroup("group_of_cool_commands")

            @command(parent=sub_group)
            async def a_very_cool_command():
                pass

    This code creates a command called ``cool_commands`` with the subcommand-group
    ``group_of_cool_commands`` that has the subcommand ``a_very_cool_command``.

    Parameters
    ----------
    name : str
        The name of the command sub-group.
    parent : :class:`~pincer.commands.groups.Group`
        The parent group of this command.
    description : Optional[:class:`str`]
        The description of the command. This has to be sent to Discord, but it does
        nothing, so it is optional.
    """

    name: str
    parent: Group
    description: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.name)
