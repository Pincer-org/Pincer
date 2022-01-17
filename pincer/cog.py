# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations
from asyncio import ensure_future

from importlib import reload, import_module
from inspect import isclass
from types import ModuleType
from typing import TYPE_CHECKING, List

from . import client as _client
from .commands.chat_command_handler import ChatCommandHandler
from .commands.interactable import Interactable
from .exceptions import CogAlreadyExists, CogNotFound

if TYPE_CHECKING:
    from typing import Type
    from .client import Client


class CogManager:
    """
    A class that can load and unload cogs
    """

    def load_cog(self, cog: Type[Cog]):
        """Load a cog from a string path, setup method in COG may
        optionally have a first argument which will contain the client!

        :Example usage:

        run.py

        .. code-block:: python3

             from pincer import Client
             from cogs.say import SayCommand

             class MyClient(Client):
                 def __init__(self, *args, **kwargs):
                     self.load_cog(SayCommand)
                     super().__init__(*args, **kwargs)

        cogs/say.py

        .. code-block:: python3

             from pincer import command

             class SayCommand(Cog):
                 @command()
                 async def say(self, message: str) -> str:
                     return message

        Parameters
        ----------
        cog : Type[:class:`~pincer.cog.Cog`]
            The cog to load.
        """
        if cog in ChatCommandHandler.managers:
            raise CogAlreadyExists(
                f"Cog `{cog}` is trying to be loaded but already exists."
            )

        cog_manager = cog(self)

        ChatCommandHandler.managers.append(cog_manager)

    def load_cogs(self, *cogs: Type[Cog]):
        """
        Loads a list of cogs

        Parameters
        ----------
        \\*cogs : Type[:class:`~pincer.cog.Cog`]
            A list of cogs to load.
        """
        for cog in cogs:
            self.load_cog(cog)

    def load_module(self, module: ModuleType):
        """Loads the cogs from a module recursively.

        Parameters
        ----------
        module : :class:`~types.ModuleType`
            The module to load.
        """
        for item in module.__dict__.values():
            if isinstance(item, ModuleType):
                self.load_module(item)
            elif isclass(item) and issubclass(item, Cog):
                self.load_cog(item)

    def reload_cog(self, cog: Type[Cog]):
        """Reloads a cog.

        Parameters
        ----------
        cog : Type[:class:`~pincer.cog.Cog`]
            The cog to load.
        """

        # Remove application commands registered to this cog
        for item in self.cogs:
            if item.name() == cog.name():
                old_cog = item
                break
        else:
            raise CogNotFound(f"Cog `{cog}` could not be found!")

        ChatCommandHandler.register = {
            key: command for key, command in ChatCommandHandler.register.items()
            if command and command.manager != old_cog
        }

        ChatCommandHandler.managers.remove(old_cog)

        # Remove events registered to this cog
        for event in vars(type(old_cog)).values():
            if isinstance(event, _client.PartialEvent):
                _client._events.pop(event.func.__name__)

        mod = reload(import_module(cog.__module__))
        new_cog = getattr(mod, cog.__name__)
        self.load_cog(new_cog)
        ChatCommandHandler.has_been_initialized = False
        ensure_future(ChatCommandHandler().initialize())

    @property
    def cogs(self) -> List[Cog]:
        """Get a dictionary of all loaded cogs.

        The key/value pair is import path/cog class.

        Returns
        -------
        List[:class:`~pincer.cog.Cog`]
            The list of cogs
        """
        return [
            manager for manager in ChatCommandHandler.managers
            if isinstance(manager, Cog)
        ]


class Cog(Interactable):
    """A cog object
    This is an object that can register commands and message components that isn't a
    client. It also can be loaded and unloaded at runtime so commands can be changed
    without restarting the bot.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

        super().__init__()

    @classmethod
    def name(cls) -> str:
        """
        Returns a unique name for this cog.

        Returns
        -------
        str
            A unique name for this cog.
        """
        return f"{cls.__module__}.{cls.__name__}"
