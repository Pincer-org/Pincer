# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is created/joined on the client"""

from ..core.dispatch import GatewayDispatch
from ..objects.guild import Guild


async def guild_create_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_guild_create``,
        generate the guild class that was created

    :param self:
        The current client.

    :param payload:
        The data received from the guild creation event.

    :return Guild:

    """
    return "on_guild_create", [
        Guild.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]


def export():
    return guild_create_middleware
