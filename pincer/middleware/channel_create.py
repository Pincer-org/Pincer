# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a channel is created/joined on the client."""
from pincer.core.dispatch import GatewayDispatch
from pincer.objects import Channel
from pincer.utils.conversion import construct_client_dict


def channel_create_middleware(self, payload: GatewayDispatch):
    """|coro|
    
    Middleware for ``on_channel_creation`` event.

    :param client:

    :param payload:
        The data received from the ready event.
        
    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_create`` and a ``Channel``
    """

    return "on_channel_create", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]
