# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message in pinned/unpinned"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.channel import ChannelPinsUpdateEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def channel_pins_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_channel_pins_update`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.gateway.GatewayDispatch`
        The data received from the channel pins update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_channel_pins_update`` and a ``Channel``
    """

    event = ChannelPinsUpdateEvent.from_dict(payload.data)
    self.channels[
        event.channel_id
    ].last_pin_timestamp = event.last_pin_timestamp

    return ("on_channel_pins_update", event)


def export():
    return channel_pins_update_middleware
