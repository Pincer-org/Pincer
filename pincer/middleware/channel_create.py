# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a channel is created/joined on the client."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.guild.channel import Channel

if TYPE_CHECKING:
    from typing import Tuple
    from ..core.gateway import GatewayDispatch
    from ..client import Client
    from ..core.gateway import Gateway


async def channel_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
) -> Tuple[str, Channel]:
    """|coro|

    Middleware for the ``on_channel_creation`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the ready event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_creation`` and a channel.
    """

    channel: Channel = Channel.from_dict(payload.data)

    self.guilds[channel.guild_id].channels.append(channel)
    self.channels[channel.id] = channel

    return "on_channel_creation", channel


def export():
    return channel_create_middleware
