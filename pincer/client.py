# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from asyncio import iscoroutinefunction, run, ensure_future
from importlib import import_module
from inspect import isasyncgenfunction
from typing import Optional, Any, Union, Dict, Tuple, List, TYPE_CHECKING

from . import __package__
from ._config import events
from .commands import ChatCommandHandler
from .core.dispatch import GatewayDispatch
from .core.gateway import Dispatcher
from .core.http import HTTPClient
from .exceptions import (
    InvalidEventName, TooManySetupArguments, NoValidSetupMethod,
    NoCogManagerReturnFound, CogAlreadyExists, CogNotFound
)
from .middleware import middleware
from .objects import User, Intents, Guild, ThrottleInterface
from .objects.app.throttling import DefaultThrottleHandler
from .utils import get_index, should_pass_cls, Coro
from .utils.signature import get_params

if TYPE_CHECKING:
    from .objects.app import AppCommand

_log = logging.getLogger(__package__)

MiddlewareType = Optional[Union[Coro, Tuple[str, List[Any], Dict[str, Any]]]]

_events: Dict[str, Optional[Union[str, Coro]]] = {}

for event in events:
    event_final_executor = f"on_{event}"

    # Event middleware for the library.
    # Function argument is a payload (GatewayDispatch).

    # The function must return a string which
    # contains the main event key.

    # As second value a list with arguments,
    # and the third value value must be a dictionary.
    # The last two are passed on as *args and **kwargs.

    # NOTE: These return values must be passed as a tuple!
    _events[event] = event_final_executor

    # The registered event by the client. Do not manually overwrite.
    _events[event_final_executor] = None


def event_middleware(call: str, *, override: bool = False):
    """
    Middleware are methods which can be registered with this decorator.
    These methods are invoked before any ``on_`` event.
    As the ``on_`` event is the final call.

    A default call exists for all events, but some might already be in
    use by the library.

    If you know what you are doing, you can override these default
    middleware methods by passing the override parameter.

    The method to which this decorator is registered must be a coroutine,
    and it must return a tuple with the following format:

    .. code-block:: python

        tuple(
            key for next middleware or final event [str],
            args for next middleware/event which will be passed as *args
                [list(Any)],
            kwargs for next middleware/event which will be passed as
                **kwargs [dict(Any)]
        )

    Two parameters are passed to the middleware. The first parameter is
    the current socket connection with and the second one is the payload
    parameter which is of type :class:`~.core.dispatch.GatewayDispatch`.
    This contains the response from the discord API.

    :Implementation example:

    .. code-block:: pycon

        >>> @event_middleware("ready", override=True)
        >>> async def custom_ready(_, payload: GatewayDispatch):
        >>>     return "on_ready", [
        >>>         User.from_dict(payload.data.get("user"))
        >>>     ]

        >>> @Client.event
        >>> async def on_ready(bot: User):
        >>>     print(f"Signed in as {bot}")


    :param call:
        The call where the method should be registered.

    Keyword Arguments:

    :param override:
        Setting this to True will allow you to override existing
        middleware. Usage of this is discouraged, but can help you out
        of some situations.
    """

    def decorator(func: Coro):
        if override:
            _log.warning(
                "Middleware overriding has been enabled for `%s`."
                " This might cause unexpected behavior.", call
            )

        if not override and callable(_events.get(call)):
            raise RuntimeError(
                f"Middleware event with call `{call}` has "
                "already been registered"
            )

        async def wrapper(cls, payload: GatewayDispatch):
            _log.debug("`%s` middleware has been invoked", call)

            return await (
                func(cls, payload)
                if should_pass_cls(func)
                else func(payload)
            )

        _events[call] = wrapper
        return wrapper

    return decorator


for event, middleware in middleware.items():
    event_middleware(event)(middleware)


class Client(Dispatcher):
    def __init__(
            self,
            token: str, *,
            received: str = None,
            intents: Intents = None,
            throttler: ThrottleInterface = DefaultThrottleHandler
    ):
        """
        The client is the main instance which is between the programmer
            and the discord API.

        This client represents your bot.

        :param token:
            The secret bot token which can be found in
            `<https://discord.com/developers/applications/<bot_id>/bot>`_

        :param received:
            The default message which will be sent when no response is
            given.

        :param intents:
            The discord intents for your client.
        """
        super().__init__(
            token,
            handlers={
                # Gets triggered on all events
                -1: self.payload_event_handler,
                # Use this event handler for opcode 0.
                0: self.event_handler
            },
            intents=intents or Intents.NONE
        )

        self.bot: Optional[User] = None
        self.received_message = received or "Command arrived successfully!"
        self.http = HTTPClient(token)
        self.throttler = throttler
        ChatCommandHandler.managers["__main__"] = self

    @property
    def chat_commands(self):
        """
        Get a list of chat command calls which have been registered in
        the ChatCommandHandler.
        """
        return [cmd.app.name for cmd in ChatCommandHandler.register.values()]

    @staticmethod
    def event(coroutine: Coro):
        """
        Register a Discord gateway event listener. This event will get
        called when the client receives a new event update from Discord
        which matches the event name.

        The event name gets pulled from your method name, and this must
        start with ``on_``.
        This forces you to write clean and consistent code.

        This decorator can be used in and out of a class, and all
        event methods must be coroutines. *(async)*

        :Example usage:

        .. code-block:: pycon

            >>> # Function based
            >>> from pincer import Client
            >>>
            >>> client = Client("token")
            >>>
            >>> @client.event
            >>> async def on_ready():
            ...     print(f"Signed in as {client.bot}")
            >>>
            >>> if __name__ == "__main__":
            ...     client.run()

        .. code-block :: pycon

            >>> # Class based
            >>> from pincer import Client
            >>>
            >>> class BotClient(Client):
            ...     @Client.event
            ...     async def on_ready(self):
            ...         print(f"Signed in as {self.bot}")
            >>>
            >>> if __name__ == "__main__":
            ...     BotClient("token").run()


        :param coroutine:
            The event its coroutine, this is the method which will be
            invoked when the event is received. Also the name of this
            coroutine is the name of the event and must always start
            with ``on_``.

        :raises TypeError:
            If the method is not a coroutine.

        :raises InvalidEventName:
            If the event name does not start with ``on_``, has already
            been registered or is not a valid event name.
        """

        if not iscoroutinefunction(coroutine) \
                and not isasyncgenfunction(coroutine):
            raise TypeError(
                "Any event which is registered must be a coroutine function"
            )

        name: str = coroutine.__name__.lower()

        if not name.startswith("on_"):
            raise InvalidEventName(
                f"The event named `{name}` must start with `on_`"
            )

        if _events.get(name) is not None:
            raise InvalidEventName(
                f"The event `{name}` has already been registered or is not "
                f"a valid event name."
            )

        _events[name] = coroutine
        return coroutine

    @staticmethod
    def get_event_coro(name: str) -> Optional[Coro]:
        call = _events.get(name.strip().lower())
        if iscoroutinefunction(call) or isasyncgenfunction(call):
            return call

    def load_cog(self, path: str):
        """
        Load a cog from a string path, setup method in COG may
        optionally have a first argument which will contain the client!

        :Example usage:

        run.py

        .. code-block:: pycon

            >>> from pincer import Client
            >>>
            >>> class BotClient(Client):
            ...     def __init__(self, *args, **kwargs):
            ...         self.load_cog("cogs.say")
            ...         super().__init__(*args, **kwargs)

        cogs/say.py

        .. code-block:: pycon

            >>> from pincer import command
            >>>
            >>> class SayCommand:
            ...     @command()
            ...     async def say(self, message: str) -> str:
            ...         return message
            >>>
            >>> setup = SayCommand


        :param path:
            The import path for the cog.
        """

        if ChatCommandHandler.managers.get(path):
            raise CogAlreadyExists(
                f"Cog `{path}` is trying to be loaded but already exists."
            )

        try:
            module = import_module(path)
        except ModuleNotFoundError:
            raise CogNotFound(f"Cog `{path}` could not be found!")

        setup = getattr(module, "setup", None)

        if not callable(setup):
            raise NoValidSetupMethod(
                f"`setup` method was expected in `{path}` but none was found!"
            )

        args, params = [], get_params(setup)

        if len(params) == 1:
            args.append(self)
        elif (length := len(params)) > 1:
            raise TooManySetupArguments(
                f"Setup method in `{path}` requested {length} arguments "
                f"but the maximum is 1!"
            )

        cog_manager = setup(*args)

        if not cog_manager:
            raise NoCogManagerReturnFound(
                f"Setup method in `{path}` didn't return a cog manager! "
                "(Did you forget to return the cog?)"
            )

        ChatCommandHandler.managers[path] = cog_manager

    @staticmethod
    def get_cogs():
        """
        Get a dictionary of all loaded cogs.

        The key/value pair is import path/cog class.
        """
        return ChatCommandHandler.managers

    async def unload_cog(self, path: str):
        """
        Unload an already loaded cog! This removes all of its commands!

        :param path:
            The path to the cog.
        """
        if not ChatCommandHandler.managers.get(path):
            raise CogNotFound(f"Cog `{path}` could not be found!")

        to_remove: List[AppCommand] = []

        for command in ChatCommandHandler.register.values():
            if not command:
                continue

            if command.call.__module__ == path:
                to_remove.append(command.app)

        await ChatCommandHandler(self).remove_commands(to_remove)

    @staticmethod
    def execute_event(call: Coro, *args, **kwargs):
        """
        Invokes an event.

        :param call:
            The call (method) to which the event is registered.

        :param \\*args:
            The arguments for the event.

        :param \\*kwargs:
            The named arguments for the event.
        """

        if should_pass_cls(call):
            args = (ChatCommandHandler.managers[call.__module__], *args)

        ensure_future(call(*args, **kwargs))

    def run(self):
        """Start the event listener"""
        self.start_loop()
        run(self.http.close())

    async def handle_middleware(
            self,
            payload: GatewayDispatch,
            key: str,
            *args,
            **kwargs
    ) -> Tuple[Optional[Coro], List[Any], Dict[str, Any]]:
        """
        Handles all middleware recursively. Stops when it has found an
        event name which starts with ``on_``.

        :param payload:
            The original payload for the event.

        :param key:
            The index of the middleware in ``_events``.

        :param \\*args:
            The arguments which will be passed to the middleware.

        :param \\*\\*kwargs:
            The named arguments which will be passed to the middleware.

        :return:
            A tuple where the first element is the final executor
            (so the event) its index in ``_events``.

            The second and third element are the ``*args``
            and ``**kwargs`` for the event.
        """
        ware: MiddlewareType = _events.get(key)
        next_call, arguments, params = ware, [], {}

        if iscoroutinefunction(ware):
            extractable = await ware(self, payload, *args, **kwargs)

            if not isinstance(extractable, tuple):
                raise RuntimeError(
                    f"Return type from `{key}` middleware must be tuple. "
                )

            next_call = get_index(extractable, 0, "")
            arguments = get_index(extractable, 1, [])
            params = get_index(extractable, 2, {})

        if next_call is None:
            raise RuntimeError(f"Middleware `{key}` has not been registered.")

        return (
            (next_call, arguments, params)
            if next_call.startswith("on_")
            else await self.handle_middleware(
                payload, next_call, *arguments, **params
            )
        )

    async def execute_error(
            self,
            error: Exception,
            name: str = "on_error",
            *args,
            **kwargs
    ):
        """
        Raises an error if no appropriate error event has been found.

        :param error:
            The error which should be raised or passed to the event.

        :param name:
            The name of the event, and how it is registered by the client.

        :param \\*args:
            The arguments for the event.

        :param \\*kwargs:
            The named arguments for the event.
        """
        if call := self.get_event_coro(name):
            self.execute_event(call, error, *args, **kwargs)
        else:
            raise error

    async def process_event(self, name: str, payload: GatewayDispatch):
        """
        Processes and invokes an event and its middleware.

        :param name:
            The name of the event, this is also the filename in the
            middleware directory.

        :param payload:
            The payload sent from the Discord gateway, this contains the
            required data for the client to know what event it is and
            what specifically happened.
        """
        try:
            key, args, kwargs = await self.handle_middleware(payload, name)

            if call := self.get_event_coro(key):
                self.execute_event(call, *args, **kwargs)

        except Exception as e:
            await self.execute_error(e)

    async def event_handler(self, _, payload: GatewayDispatch):
        """
        Handles all payload events with opcode 0.

        :param _:
            Socket param, but this isn't required for this handler. So
            its just a filler parameter, doesn't matter what is passed.

        :param payload:
            The payload sent from the Discord gateway, this contains the
            required data for the client to know what event it is and
            what specifically happened.
        """
        await self.process_event(payload.event_name.lower(), payload)

    async def payload_event_handler(self, _, payload: GatewayDispatch):
        """
        Special event which activates on_payload event!

        :param _:
            Socket param, but this isn't required for this handler. So
            its just a filler parameter, doesn't matter what is passed.

        :param payload:
            The payload sent from the Discord gateway, this contains the
            required data for the client to know what event it is and
            what specifically happened.
        """
        await self.process_event("payload", payload)

    async def get_guild(self, guild_id: int) -> Guild:
        """
        Fetch a guild object by the guild identifier.

        :param guild_id:
            The id of the guild which should be fetched from the Discord
            gateway.

        :returns:
            A Guild object.
        """
        return await Guild.from_id(self, guild_id)

    async def get_user(self, _id: int) -> User:
        """
        Fetch a User from its identifier

        :param _id:
            The id of the user which should be fetched from the Discord
            gateway.

        :returns:
            A User object.
        """
        return await User.from_id(self, _id)


Bot = Client
