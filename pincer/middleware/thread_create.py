# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is created/joined on the client."""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


def thread_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_thread_create`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the thread create event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_thread_create`` and an ``Channel``
    """

    return "on_thread_create", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return thread_create_middleware
