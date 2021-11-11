# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is updated"""
from typing import List

from ..core.dispatch import GatewayDispatch
from ..objects import Guild, Channel
from ..utils.conversion import construct_client_dict


async def guild_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.guild.Guild`]]
        ``on_guild_Update`` and an ``Guild``
    """

    channel_list = payload.data.pop("channels", [])

    channels: List[Channel] = [
        Channel.from_dict(construct_client_dict(self, channel))
        for channel in channel_list
    ]

    guild = Guild.from_dict(construct_client_dict(
        self,
        {"channels": channels, **payload.data}
    ))
    self.guild[guild.id] = guild

    return "on_guild_update", [guild]


def export():
    return guild_update_middleware
