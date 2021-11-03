# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a channel is created/joined on the client."""
from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


def channel_create_middleware(self, payload: GatewayDispatch):
    """|coro|
    
    Middleware for ``on_channel_creation`` event.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot

    payload : :class:`GatewayDispatch`
        The data recieved from the channel create event
        
    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_create`` and a ``Channel``
    """

    return "on_channel_create", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]

def export() -> Coro:
    return channel_create_middleware
