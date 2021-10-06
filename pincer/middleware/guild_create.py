# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is created/joined on the client"""

from ..core.dispatch import GatewayDispatch
from ..objects.guild import Guild

async def guild_create_middleware(self, payload: GatewayDispatch):
    return "on_guild_create", [
        Guild.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]

def export():
    return guild_create_middleware
