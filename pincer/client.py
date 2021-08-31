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
from typing import Optional, TypeVar, Callable, Coroutine, Any, Union

from pincer import __package__
from pincer._config import GatewayConfig
from pincer.core.dispatch import GatewayDispatch
from pincer.core.gateway import Dispatcher
from pincer.core.http import HTTPClient
from pincer.exceptions import InvalidEventName
from pincer.objects.user import User

_log = logging.getLogger(__package__)

Coro = TypeVar('Coro', bound=Callable[..., Coroutine[Any, Any, Any]])


class Client(Dispatcher):
    """
    The main instance which the user will interact with.
    """

    def __init__(self, token: str):
        # TODO: Write docs
        # TODO: Implement intents
        super().__init__(
            token,
            handlers={
                0: self.event_handler
            }
        )

        self.http = HTTPClient(token, GatewayConfig.version)
        self.bot: Optional[User] = None

        self.__events = {
            "ready": self.__on_ready,
            "on_ready": None,
            "channel_create": "on_channel_create",
            "on_channel_create": None,
            "channel_update": "on_channel_update",
            "on_channel_update": None,
            "channel_delete": "on_channel_delete",
            "on_channel_delete": None,
            "channel_pin_update": "on_channel_pin_update",
            "on_channel_pin_update": None,
            "thread_create": "on_thread_create",
            "on_thread_create": None,
            "thread_update": "on_thread_update",
            "on_thread_update": None,
            "thread_delete": "on_thread_delete",
            "on_thread_delete": None,
            "thread_member_update": "on_thread_member_update",
            "on_thread_member_update": None,
            "thread_members_update": "on_thread_members_update",
            "on_thread_members_update": None,
            "guild_create": "on_guild_create",
            "on_guild_create": None,
            "guild_update": "on_guild_update",
            "on_guild_update": None,
            "guild_delete": "on_guild_delete",
            "on_guild_delete": None,
            "guild_ban_add": "on_guild_ban_add",
            "on_guild_ban_add": None,
            "guild_ban_remove": "on_guild_ban_remove",
            "on_guild_ban_remove": None,
            "guild_emoji_update": "on_guild_emoji_update",
            "on_guild_emoji_update": None,
            "guild_stickers_update": "on_guild_stickers_update",
            "on_guild_stickers_update": None,
            "guild_integrations_update": "on_guild_integrations_update",
            "on_guild_integrations_update": None,
            "guild_member_add": "on_guild_member_add",
            "on_guild_member_add": None,
            "guild_member_remove": "on_guild_member_remove",
            "on_guild_member_remove": None,
            "guild_members_chunk": "on_guild_members_chunk",
            "on_guild_members_chunk": None,
            "guild_role_create": "on_guild_role_create",
            "on_guild_role_create": None,
            "guild_role_update": "on_guild_role_update",
            "on_guild_role_update": None,
            "guild_role_delete": "on_guild_role_delete",
            "on_guild_role_delete": None,
            "integration_create": "on_integration_create",
            "on_integration_create": None,
            "integration_update": "on_integration_update",
            "on_integration_update": None,
            "integration_delete": "on_integration_delete",
            "on_integration_delete": None,
            "invite_create": "on_invite_create",
            "on_invite_create": None,
            "messages_create": "on_messages_create",
            "on_messages_create": None,
            "message_update": "on_message_update",
            "on_message_update": None,
            "message_delete": "on_message_delete",
            "on_message_delete": None,
            "message_delete_bulk": "on_message_delete_bulk",
            "on_message_delete_bulk": None,
            "message_reaction_add": "on_message_reaction_add",
            "on_message_reaction_add": None,
            "message_reaction_remove": "on_message_reaction_remove",
            "on_message_reaction_remove": None,
            "message_reaction_remove_all": "on_message_reaction_remove_all",
            "on_message_reaction_remove_all": None,
            "message_reaction_remove_emoji": "on_message_reaction_remove_emoji",
            "on_message_reaction_remove_emoji": None,
            "presence_update": "on_presence_update",
            "on_presence_update": None,
            "stage_instance_create": "on_stage_instance_create",
            "on_stage_instance_create": None,
            "stage_instance_update": "on_stage_instance_update",
            "on_stage_instance_update": None,
            "stage_instance_delete": "on_stage_instance_delete",
            "on_stage_instance_delete": None,
            "typing_start": "on_typing_start",
            "on_typing_start": None,
            "voice_state_update": "on_voice_state_update",
            "on_voice_state_update": None,
            "voice_server_update": "on_voice_server_update",
            "on_voice_server_update": None,
            "webhooks_update": "on_webhooks_update",
            "on_webhooks_update": None,
        }

    def event(self, coroutine: Coro):
        if not iscoroutinefunction(coroutine):
            raise TypeError("Any event which is registered must be a coroutine "
                            "function")

        name: str = coroutine.__name__.lower()

        if not name.startswith("on_"):
            raise InvalidEventName(
                f"The event `{name}` its name must start with `on_`"
            )

        if self.__events.get(name) is not None:
            raise InvalidEventName(
                f"The event `{name}` has already been registered or is not "
                f"a event name."
            )

        self.__events[name] = coroutine
        return coroutine

    async def event_handler(self, _, payload: GatewayDispatch):
        middleware: Optional[Union[Coro, str]] = self.__events.get(
            payload.event_name.lower()
        )

        if iscoroutinefunction(middleware):
            final_call, params = await middleware(payload)
        else:
            final_call, params = middleware, dict()

        final_call: str = final_call
        params: dict = params

        final_call_routine: Optional[Coro] = self.__events.get(final_call)

        if iscoroutinefunction(final_call_routine):
            await final_call_routine(**params)

    async def __on_ready(self, payload: GatewayDispatch):
        self.bot = User.from_dict(payload.data.get("user"))
        return "on_ready", dict()


Bot = Client
