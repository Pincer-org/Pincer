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
import logging
from asyncio import iscoroutinefunction
from inspect import getfullargspec
from typing import (
    Optional, TypeVar, Callable, Coroutine, Any, Union, Dict, Tuple, List
)

from pincer import __package__
from pincer._config import GatewayConfig, events
from pincer.core.dispatch import GatewayDispatch
from pincer.core.gateway import Dispatcher
from pincer.core.http import HTTPClient
from pincer.exceptions import InvalidEventName
from pincer.objects.user import User
from pincer.utils.extraction import get_index

_log = logging.getLogger(__package__)

Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])
middleware_type = Optional[Union[Coro, Tuple[str, List[Any], Dict[str, Any]]]]

_events: Dict[str, Optional[Union[str, Coro]]] = {}

for event in events:
    event_final_executor = f"on_{event}"

    # Event middleware for the library. Function argument is a payload
    # (GatewayDispatch). The function must return a string which
    # contains the main event key. As second value a list with arguments,
    # and thee third value value must be a dictionary. The last two are
    # passed on as *args and **kwargs.
    #
    # NOTE: These return values must be passed as a tuple!
    _events[event] = event_final_executor

    # The registered event by the client. Do not manually overwrite.
    _events[event_final_executor] = None


class Client(Dispatcher):
    def __init__(self, token: str):
        """
        The client is the main instance which is between the programmer and the
        discord API. This client represents your bot.

        :param token: The secret bot token which can be found in
            https://discord.com/developers/applications/<bot_id>/bot.
        """
        # TODO: Implement intents
        super().__init__(
            token,
            handlers={
                # Use this event handler for opcode 0.
                0: self.event_handler
            }
        )
        global _events

        # TODO: close the client after use
        self.http = HTTPClient(token, version=GatewayConfig.version)
        self.bot: Optional[User] = None
        _events["ready"] = self.__on_ready

    @staticmethod
    def event(coroutine: Coro):
        # TODO: Write docs
        global _events

        if not iscoroutinefunction(coroutine):
            raise TypeError("Any event which is registered must be a coroutine "
                            "function")

        name: str = coroutine.__name__.lower()

        if not name.startswith("on_"):
            raise InvalidEventName(
                f"The event `{name}` its name must start with `on_`"
            )

        if _events.get(name) is not None:
            raise InvalidEventName(
                f"The event `{name}` has already been registered or is not "
                f"a valid event name."
            )

        _events[name] = coroutine
        return coroutine

    async def event_handler(self, _, payload: GatewayDispatch):
        # TODO: Write docs
        event_name = payload.event_name.lower()
        middleware: middleware_type = _events.get(event_name)
        final_call, args, params = middleware, list(), dict()

        if iscoroutinefunction(middleware):
            extractable = await middleware(payload)
            final_call = get_index(extractable, 0, f"on_{event_name}")
            args = get_index(extractable, 1, list())
            params = get_index(extractable, 2, dict())

        final_call_routine: Optional[Coro] = _events.get(final_call)

        if iscoroutinefunction(final_call_routine):
            kwargs = params
            arguments = getfullargspec(final_call_routine).args
            if len(arguments) >= 1 and arguments[0] == "self":
                kwargs["self"] = self

            await final_call_routine(*args, **kwargs)

    async def __on_ready(self, payload: GatewayDispatch):
        # TODO: Write docs
        self.bot = User.from_dict(payload.data.get("user"))
        return "on_ready",


Bot = Client
