# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

from .chat_command_handler import ChatCommandHandler
from ..objects.app.command import ClientCommandStructure

_log = logging.getLogger(__name__)


class PartialInteractable:
    def __init__(self, key: int, value: ClientCommandStructure) -> None:
        self.key = key
        self.value = value

    def register(self, manager: Any):
        _log.info(
            f"Registered command `{self.value.app.name}` to"
            f" `{self.value.call.__name__}` locally."
        )
        self.value.manager = manager
        ChatCommandHandler.register[self.key] = self.value

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.value.call(*args, **kwds)


class Interactable:
    def __init__(self) -> None:
        for item in self.__class__.__dict__.values():
            if isinstance(item, PartialInteractable):
                item.register(self)
