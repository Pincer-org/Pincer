# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects.guild import UnavailableGuild
from ..utils.conversion import construct_client_dict


async def guild_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_delete`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild delete event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.guild.UnavailableGuild`]]
        ``on_guild_delete`` and an ``UnavailableGuild``
    """
    guild = UnavailableGuild.from_dict(construct_client_dict(self, payload.data))

    if guild.id in self.guilds.key():
        self.guilds.pop(guild.id)

    return "on_guild_delete", [guild]


def export():
    return guild_delete_middleware
