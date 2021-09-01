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

from dataclasses import dataclass


@dataclass
class GatewayConfig:
    """
    This file is to make maintaining the library its gateway
    configuration easier.
    """
    socket_base_url: str = "wss://gateway.discord.gg/"
    version: int = 9
    encoding: str = "json"

    # TODO: Implement compression
    # compress: str = "zlib-stream"

    @staticmethod
    def uri() -> str:
        """
        :return uri:
            The GatewayConfig's uri.
        """
        return (
            f"{GatewayConfig.socket_base_url}"
            f"?v={GatewayConfig.version}"
            f"&encoding={GatewayConfig.encoding}"
        )


events = [
    "ready", "channel_create", "channel_update", "channel_delete",
    "channel_pin_update", "thread_create", "thread_update",
    "thread_delete", "thread_member_update", "thread_members_update",
    "guild_create", "guild_update", "guild_delete", "guild_ban_add",
    "guild_ban_remove", "guild_emoji_update", "guild_stickers_update",
    "guild_integrations_update", "guild_member_add",
    "guild_member_remove", "guild_members_chunk", "guild_role_create",
    "guild_role_update", "guild_role_delete", "integration_create",
    "integration_update", "integration_delete", "invite_create",
    "messages_create", "message_update", "message_delete",
    "message_delete_bulk", "message_reaction_add",
    "message_reaction_remove", "message_reaction_remove_all",
    "message_reaction_remove_emoji", "presence_update", "stage_instance_create",
    "stage_instance_update", "stage_instance_delete", "typing_start",
    "voice_state_update", "voice_server_update", "webhooks_update"
]
