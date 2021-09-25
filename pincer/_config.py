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
