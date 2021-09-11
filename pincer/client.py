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
from typing import Optional, Any, Union, Dict, Tuple, List

from . import __package__
from ._config import events
from .commands import ChatCommandHandler
from .core.dispatch import GatewayDispatch
from .core.gateway import Dispatcher
from .core.http import HTTPClient
from .exceptions import InvalidEventName
from .objects import User, Message, Embed
from .objects.interactions import Interaction, InteractionFlags
from .utils import get_index, should_pass_cls, Coro, MISSING
from .utils.extraction import get_params

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


def middleware(call: str, *, override: bool = False):
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

        >>> @middleware("ready", override=True)
        >>> async def custom_ready(_, payload: GatewayDispatch):
        >>>     return "on_ready", [User.from_dict(payload.data.get("user"))]

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
                else await func(payload)
            )

        _events[call] = wrapper
        return wrapper

    return decorator


class Client(Dispatcher):
    def __init__(self, token: str, *, received: str = None):
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
        """
        # TODO: Implement intents
        super().__init__(
            token,
            handlers={
                # Use this event handler for opcode 0.
                0: self.event_handler
            }
        )

        self.bot: Optional[User] = None
        self.__received = received or "Command arrived successfully!"
        self.__token = token

    @property
    def http(self):
        """
        Returns a http client with the current client its
        authentication credentials.

        :Usage example:

        .. code-block:: pycon

            >>> async with self.http as client:
            >>>     await client.post(
            ...         '<endpoint>',
            ...         {
            ...             "foo": "bar",
            ...             "bar": "baz",
            ...             "baz": "foo"
            ...         }
            ...    )

        """
        return HTTPClient(self.__token)

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
        start with ``on_``. This forces you to write clean and consistent
        code.

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


        :param coroutine: # TODO: add info

        :raises TypeError:
            If the method is not a coroutine.

        :raises InvalidEventName:
            If the event name does not start with ``on_``, has already
            been registered or is not a valid event name.
        """

        if not iscoroutinefunction(coroutine):
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
            (so the event) its index in ``_events``. The second and third
            element are the ``*args`` and ``**kwargs`` for the event.
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
        event_name = payload.event_name.lower()

        key, args, kwargs = await self.handle_middleware(payload, event_name)

        call = _events.get(key)

        if iscoroutinefunction(call):
            if should_pass_cls(call):
                await call(self, *args, **kwargs)
            else:
                await call(*args, **kwargs)

    @middleware("ready")
    async def on_ready_middleware(self, payload: GatewayDispatch):
        """
        Middleware for ``on_ready`` event.

        :param payload:
            The data received from the ready event.
        """
        self.bot = User.from_dict(payload.data.get("user"))
        await ChatCommandHandler(self).initialize()
        return "on_ready",

    @middleware("interaction_create")
    async def on_interaction_middleware(self, payload: GatewayDispatch):
        """
        Middleware for ``on_interaction``, which handles command
        execution.

        :param payload:
            The data received from the interaction event.
        """
        interaction: Interaction = Interaction.from_dict(payload.data)
        command = ChatCommandHandler.register.get(interaction.data.name)

        if command:
            defaults = {param: None for param in get_params(command.call)}
            params = {}

            if interaction.data.options is not MISSING:
                params = {
                    opt.name: opt.value for opt in interaction.data.options
                }

            kwargs = {**defaults, **params}

            if should_pass_cls(command.call):
                kwargs["self"] = self

            message = await command.call(**kwargs)

            if isinstance(message, Embed):
                message = Message(embeds=[message])

            elif not isinstance(message, Message):
                message = Message(message) if message else Message(
                    self.__received,
                    flags=InteractionFlags.EPHEMERAL
                )

            async with self.http as http:
                await http.post(
                    f"interactions/{interaction.id}/{interaction.token}/callback",
                    message.to_dict()
                )

        return "on_interaction_create", [interaction]


Bot = Client
