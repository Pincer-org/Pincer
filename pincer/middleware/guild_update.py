# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is updated"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Guild

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.guild.Guild`]
        ``on_guild_Update`` and an ``Guild``
    """

    guild = Guild.from_dict(payload.data)
    self.guilds[guild.id] = guild

    for channel in guild.channels:
        self.channels[channel.id] = channel

    return "on_guild_update", guild


def export():
    return guild_update_middleware
