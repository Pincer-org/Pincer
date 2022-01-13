# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is created/joined on the client"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.guild import Guild

if TYPE_CHECKING:
    from typing import Tuple
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_create``,
        generate the guild class that was created

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild create event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.guild.Guild`]

        ``on_guild_create`` and a ``Guild``
    """
    guild = Guild.from_dict(payload.data)
    self.guilds[guild.id] = guild
    for channel in guild.channels:
        self.channels[channel.id] = channel

    return "on_guild_create", guild


def export():
    return guild_create_middleware
