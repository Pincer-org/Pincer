# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Any, List, Tuple, Union, T

from ..utils.types import MISSING
from ..objects.app.command import AppCommandOptionChoice


class _CommandTypeMeta(type):
    def __getitem__(cls, args: Union[Tuple, Any]):
        if not isinstance(args, tuple):
            args = args,

        return cls(*args)


class CommandArg(metaclass=_CommandTypeMeta):
    """Holds all application command options"""

    def __init__(self, command_type, *args) -> None:
        self.command_type = command_type
        self.modifiers = args

    def get_arg(self, arg_type: T) -> T:
        for arg in self.modifiers:
            if type(arg) == arg_type:
                return arg.get_payload()

        return MISSING


class Description(metaclass=_CommandTypeMeta):
    """Represents the description application command option type"""

    def __init__(self, desc) -> None:
        self.desc = str(desc)

    def get_payload(self) -> str:
        return self.desc


class Choice(metaclass=_CommandTypeMeta):
    """Represents an application command choice"""

    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value


class Choices(metaclass=_CommandTypeMeta):
    """Represents the choice application command option type"""

    def __init__(self, *choices) -> None:
        self.choices = []

        for choice in choices:
            if isinstance(choice, Choice):
                self.choices.append(AppCommandOptionChoice(
                    name=choice.name,
                    value=choice.value
                ))
                continue

            self.choices.append(AppCommandOptionChoice(
                name=str(choice),
                value=choice
            ))

    def get_payload(self) -> List[Union[str, int, float]]:
        return self.choices
