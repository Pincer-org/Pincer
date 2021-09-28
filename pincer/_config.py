# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

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
    compression: str = "zlib-stream"

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
    "channel_create", "channel_delete", "channel_pin_update", "channel_update",
    "guild_ban_add", "guild_ban_remove",  "guild_create", "guild_delete",
    "guild_emoji_update", "guild_integrations_update", "guild_member_add",
    "guild_member_remove", "guild_members_chunk", "guild_role_create",
    "guild_role_delete", "guild_role_update", "guild_stickers_update",
    "guild_update", "integration_create", "integration_delete",
    "integration_update", "invite_create", "message_delete",
    "message_delete_bulk", "message_reaction_add", "message_reaction_remove",
    "message_reaction_remove_all",  "message_reaction_remove_emoji",
    "message_update", "messages_create", "presence_update", "ready",
    "stage_instance_create", "stage_instance_delete", "stage_instance_update",
    "thread_create", "thread_delete", "thread_member_update",
    "thread_members_update", "thread_update", "typing_start",
    "voice_server_update", "voice_state_update", "webhooks_update"
]
