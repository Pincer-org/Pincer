# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message in pinned/unpinned"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.channel import ChannelPinsUpdateEvent


async def channel_pins_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_channel_pins_update`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the channel pins update event.

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
