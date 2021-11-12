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
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the channel delete event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_delete`` and a ``Channel``
    """

    channel = Channel.from_dict(construct_client_dict(self, payload.data))

    if channel.guild_id in self.guilds:
        guild = self.guilds[channel.guild_id]
        old = filter(lambda c: c.id == channel.id, guild.channels)
        if old:
            guild.channels.remove(old)

    return "on_channel_delete", [channel]


def export():
    return channel_delete_middleware
