# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

import logging
from typing import Any, List, Tuple, Union, T

from ..utils.types import MISSING
from ..objects.app.command import AppCommandOptionChoice

_log = logging.getLogger(__name__)


class _CommandTypeMeta(type):
    def __getitem__(cls, args: Union[Tuple, Any]):
        if not isinstance(args, tuple):
            args = (args,)

        return cls(*args)


class CommandArg(metaclass=_CommandTypeMeta):
    """
    Holds the parameters of an application command option

    .. note::
        Deprecated. :class:`typing.Annotated` or :class:`typing_extensions.Annotated`
        should be used instead. See
        https://docs.pincer.dev/en/stable/interactions.html#arguments for more
        information.

    .. code-block:: python3

        Annotated[
            # This is the type of command.
            # Supported types are str, int, bool, float, User, Channel, and Role
            int,
            # The modifiers to the command go here
            Description("Pick a number 1-10"),
            MinValue(1),
            MaxValue(10)
        ]

    Parameters
    ----------
    command_type : T
        The type of the command
    \\*args : :class:`~pincer.commands.arg_types.Modifier`

    """

    def __init__(self, command_type, *args):
        self.command_type = command_type
        self.modifiers = args
        _log.warning(
            "CommandArg is deprecated and will be removed in future releases."
            " `typing.Annotated`/`typing_extensions.Annotated.` should be used instead."
            " See https://docs.pincer.dev/en/stable/interactions.html#arguments for"
            " more information."
        )

    def get_arg(self, arg_type: T) -> T:
        for arg in self.modifiers:
            if isinstance(arg, arg_type):
                return arg.get_payload()

        return MISSING


class Modifier(metaclass=_CommandTypeMeta):
    """
    Modifies a CommandArg by being added to
    :class:`~pincer.commands.arg_types.CommandArg`'s args.

    Modifiers go inside an :class:`typing.Annotated` type hint.

    .. code-block:: python3

        Annotated[
            # This is the type of command.
            # Supported types are str, int, bool, float, User, Channel, and Role
            int,
            # The modifiers to the command go here
            Description("Pick a number 1-10"),
            MinValue(1),
            MaxValue(10)
        ]

    """


class Description(Modifier):
    """
    Represents the description of an application command option

    .. code-block:: python3

        # Creates an int argument with the description "example description"
        Annotated[
            int,
            Description("example description")
        ]

    Parameters
    ----------
    desc : str
        The description for the command.
    """

    def __init__(self, desc):
        self.desc = str(desc)

    def get_payload(self) -> str:
        return self.desc


class Choice(Modifier):
    """
    Represents a choice that the user can pick from

    .. code-block:: python3

        Choices(
            Choice("First Number", 10),
            Choice("Second Number", 20)
        )

    Parameters
    ----------
    name : str
        The name of the choice
    value : Union[int, str, float]
        The value of the choice
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Choices(Modifier):
    """
    Represents a group of application command choices that a user can pick from

    .. code-block:: python3

        Annotated[
            int,
            Choices(
                Choice("First Number", 10),
                20,
                50
            )
        ]

    Parameters
    ----------
    \\*choices : Union[:class:`~pincer.commands.arg_types.Choice`, str, int, float]
        A choice. If the type is not :class:`~pincer.commands.arg_types.Choice`,
        the same value will be used for the choice name and value.
    """

    def __init__(self, *choices):
        self.choices = []

        for choice in choices:
            if isinstance(choice, Choice):
                self.choices.append(
                    AppCommandOptionChoice(name=choice.name, value=choice.value)
                )
                continue

            self.choices.append(
                AppCommandOptionChoice(name=str(choice), value=choice)
            )

    def get_payload(self) -> List[AppCommandOptionChoice]:
        return self.choices


class ChannelTypes(Modifier):
    """
    Represents a group of channel types that a user can pick from

    .. code-block:: python3

        Annotated[
            Channel,
            # The user will only be able to choice between GUILD_TEXT and
            GUILD_TEXT channels.
            ChannelTypes(
                ChannelType.GUILD_TEXT,
                ChannelType.GUILD_VOICE
            )
        ]

    Parameters
    ----------
    \\*types : :class:`~pincer.objects.guild.channel.ChannelType`
        A list of channel types that the user can pick from.
    """

    def __init__(self, *types):
        self.types = types

    def get_payload(self):
        return self.types


class MaxValue(Modifier):
    """
    Represents the max value for a number

    .. code-block:: python3

        Annotated[
            int,
            # The user can't pick a number above 10
            MaxValue(10)
        ]

    Parameters
    ----------
    max_value : Union[:class:`float`, :class:`int`]
        The max value a user can choose.
    """

    def __init__(self, max_value):
        self.max_value = max_value

    def get_payload(self):
        return self.max_value


class MinValue(Modifier):
    """
    Represents the minimum value for a number

    .. code-block:: python3

        Annotated[
            int,
            # The user can't pick a number below 10
            MinValue(10)
        ]

    Parameters
    ----------
    min_value : Union[:class:`float`, :class:`int`]
        The minimum value a user can choose.
    """

    def __init__(self, min_value):
        self.min_value = min_value

    def get_payload(self):
        return self.min_value
