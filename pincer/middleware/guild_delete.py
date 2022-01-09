# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is deleted"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.guild import UnavailableGuild

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_delete_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild delete event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.guild.UnavailableGuild`]
        ``on_guild_delete`` and an ``UnavailableGuild``
    """

    guild = UnavailableGuild.from_dict(payload.data)

    self.guilds.pop(guild.id, None)

    for channel in self.guild.channels:
        self.channels.pop(channel.id, None)

    return "on_guild_delete", guild


def export():
    return guild_delete_middleware
