# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is deleted"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Channel

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def thread_delete_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_thread_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the thread delete event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_thread_delete`` and an ``Channel``
    """

    channel = Channel.from_dict(payload.data)

    guild = self.guilds.get(channel.guild_id)
    if guild:
        guild.threads = [c for c in guild.threads if c.id != channel.id]

    self.channels.pop(channel.id, None)

    return "on_thread_delete", channel


def export():
    return thread_delete_middleware
