# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message in pinned/unpinned"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.channel import ChannelPinsUpdateEvent
from ..utils import Timestamp


async def channel_pins_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_channel_pins_update``,
        creates a object for the message pinned/unpinned

    :param self:
        The current client.

    :param payload:
        The data received from the channel pins update event.
    """
    return "on_channel_pins_update", [
        ChannelPinsUpdateEvent.from_dict(payload.data)
    ]


def export():
    return channel_pins_update_middleware
