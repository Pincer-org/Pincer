# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is created/joined on the client."""

from ..core.dispatch import GatewayDispatch
from ..utils.conversion import construct_client_dict
from ..objects import Channel


async def thread_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_thread_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the thread create event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_thread_create`` and an ``Channel``
    """

    channel: Channel = Channel.from_dict(
        construct_client_dict(self, payload.data)
    )

    if self.guilds[channel.guild_id].threads:
        self.guilds[channel.guild_id].threads.append(channel)
    else:
        self.guilds[channel.guild_id].threads = [channel]

    self.channels[channel.id] = channel

    return "on_thread_create", channel


def export():
    return thread_create_middleware
