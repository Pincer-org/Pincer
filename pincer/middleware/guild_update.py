# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects import Guild
from ..utils.conversion import construct_client_dict


async def guild_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_guild_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.guild.Guild`]
        ``on_guild_Update`` and an ``Guild``
    """

    guild = Guild.from_dict(construct_client_dict(self, payload.data))
    self.guild[guild.id] = guild

    for channel in guild.channels:
        self.channels[channel.id] = channel

    return "on_guild_update", guild


def export():
    return guild_update_middleware
