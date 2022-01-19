# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from collections import ChainMap

from .. import client as _client
from .chat_command_handler import ChatCommandHandler, _hash_interactable_structure
from .components.component_handler import ComponentHandler
from ..objects.app.command import AppCommand, InteractableStructure


INTERACTION_REGISTERS = ChainMap(ChatCommandHandler.register, ComponentHandler.register)


class Interactable:
    """
    Class that can register :class:`~pincer.commands.interactable.PartialInteractable`
    objects. Any class that subclasses this class can register Application Commands and
    Message Components.
    PartialInteractable objects are registered by running the register function and
    setting an attribute of the client to the result.
    """

    def __init__(self):
        for value in vars(type(self)).values():
            if isinstance(value, InteractableStructure):
                value.manager = self

    def __del__(self):
        self.unassign()

    def unassign(self):
        for value in vars(type(self)).values():
            if isinstance(value, InteractableStructure):
                if isinstance(value.metadata, AppCommand):
                    INTERACTION_REGISTERS.pop(
                        _hash_interactable_structure(value),
                        None
                    )

                _client._events.pop(
                    value.call.__name__.lower(), None
                )
