# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is updated"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Channel
from ..utils import replace

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def thread_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_thread_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the thread update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_thread_update`` and an ``Channel``
    """

    channel = Channel.from_dict(payload.data)
    guild = self.guilds.get(channel.guild_id)

    if guild:
        guild.threads = replace(
            lambda _channel: _channel.id == channel.id,
            self.guilds[channel.guild_id].threads,
            channel,
        )
        self.channels[channel.id] = channel

    return "on_thread_update", channel


def export():
    return thread_update_middleware
