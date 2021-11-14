# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Channel Middlewares"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.dispatch import GatewayDispatch
from ..objects.guild.channel import Channel
from ..utils.conversion import construct_client_dict
from ..objects.events.channel import ChannelPinsUpdateEvent

if TYPE_CHECKING:
    from typing import List, Tuple

def channel_create_middleware(
    self, payload: GatewayDispatch
) -> Tuple[str, List[Channel]]:
    """|coro|

    Middleware for ``on_channel_creation`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``"on_channel_creation"`` and a channel.
    """
    return "on_channel_creation", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


async def channel_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_channel_delete``,

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the channel delete event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_delete`` and a ``Channel``
    """

    channel = Channel.from_dict(construct_client_dict(self, payload.data))

    if channel.guild_id in self.guilds:
        guild = self.guilds[channel.guild_id]
        old = filter(lambda c: c.id == channel.id, guild.channels)
        if old:
            guild.channels.remove(old)

    return "on_channel_delete", [channel]


async def channel_pins_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_channel_pins_update``,

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the channel pins update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_pins_update`` and a ``Channel``
    """

    return "on_channel_pins_update", [ChannelPinsUpdateEvent.from_dict(payload.data)]


async def channel_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_channel_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the channel update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.channel.channel.Channel`]]
        ``on_channel_update`` and a ``Channel``
    """

    channel = Channel.from_dict(construct_client_dict(self, payload.data))

    if channel.guild_id in self.guilds.keys():
        guild = self.guilds[channel.guild_id]
        old = filter(lambda c: c.id == channel.id, guild.channels)
        if old:
            guild.channels.remove(old)
        guild.channels.append(channel)

    return "on_channel_update", [channel]


def export():
    return (
        channel_create_middleware,
        channel_delete_middleware,
        channel_pins_update_middleware,
    )
