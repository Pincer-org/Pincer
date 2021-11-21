# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from typing import Any, Tuple, Union


class _CommandTypeMeta(type):
    def __getitem__(cls, args: Union[Tuple, Any]):
        if not isinstance(args, tuple):
            args = args,

        return cls(*args)


"""Valid for all Command Types"""


class CommandArg(metaclass=_CommandTypeMeta):
    def __init__(self, command_type, *args) -> None:
        self.command_type = command_type
        self.modifiers = args


class Description(metaclass=_CommandTypeMeta):
    def __init__(self, desc) -> None:
        self.desc = desc


class Name(metaclass=_CommandTypeMeta):
    def __init__(self, name) -> None:
        self.name = name


class OptionalArg(metaclass=type):
    pass
