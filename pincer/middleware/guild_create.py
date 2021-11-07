# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is created/joined on the client"""

from ..core.dispatch import GatewayDispatch
from ..objects.guild import Guild
from ..utils.conversion import construct_client_dict


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
    guild = Guild.from_dict(construct_client_dict(self, payload.data))
    self.guilds[guild.id] = guild
    return "on_guild_create", [guild]


def export():
    return guild_create_middleware
