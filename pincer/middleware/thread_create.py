# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is created/joined on the client."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Channel

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def thread_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_thread_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the thread create event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_thread_create`` and an ``Channel``
    """

    channel: Channel = Channel.from_dict(payload.data)

    if self.guilds[channel.guild_id].threads:
        self.guilds[channel.guild_id].threads.append(channel)
    else:
        self.guilds[channel.guild_id].threads = [channel]

    self.channels[channel.id] = channel

    return "on_thread_create", channel


def export():
    return thread_create_middleware
