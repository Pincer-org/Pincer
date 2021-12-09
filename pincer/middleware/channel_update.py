# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a channel is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


async def channel_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_channel_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the channel update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.channel.channel.Channel`]
        ``on_channel_update`` and a ``Channel``
    """

    channel = Channel.from_dict(construct_client_dict(self, payload.data))
    self.channels[channel.id] = channel

    return "on_channel_update", channel


def export():
    return channel_update_middleware
