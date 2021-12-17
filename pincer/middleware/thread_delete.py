# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


async def thread_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_thread_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the thread delete event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.channel.Channel`]
        ``on_thread_delete`` and an ``Channel``
    """

    channel = Channel.from_dict(construct_client_dict(self, payload.data))

    guild = self.guilds.get(channel.guild_id)
    if guild:
        guild.threads = [
            c for c in guild.threads if c.id != channel.id
        ]

    self.channels.pop(channel.id, None)

    return "on_thread_delete", channel


def export():
    return thread_delete_middleware
