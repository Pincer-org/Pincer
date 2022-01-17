# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a channel is deleted"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Channel

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def channel_delete_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_channel_delete`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.gateway.GatewayDispatch`
        The data received from the channel delete event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_channel_delete`` and a ``Channel``
    """

    channel = Channel.from_dict(payload.data)

    guild = self.guilds.get(channel.guild_id)
    if guild:
        guild.channels = [c for c in guild.channels if c.id != channel.id]

    self.channels.pop(channel.id, None)

    return "on_channel_delete", channel


def export():
    return channel_delete_middleware
