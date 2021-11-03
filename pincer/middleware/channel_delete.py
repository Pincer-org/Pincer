# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a channel is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


async def channel_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_channel_delete``,

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.

    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the channel delete event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_delete`` and a ``Channel``
    """
    return "on_channel_delete", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return channel_delete_middleware
