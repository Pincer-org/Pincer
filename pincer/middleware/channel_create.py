# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Sent when a channel is created/joined on the client."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.guild.channel import Channel
from ..utils.conversion import construct_client_dict

if TYPE_CHECKING:
    from typing import Tuple
    from ..core.dispatch import GatewayDispatch


async def channel_create_middleware(
    self, payload: GatewayDispatch
) -> Tuple[str, Channel]:
    """|coro|

    Middleware for the ``on_channel_creation`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.channel.Channel`]]
        ``on_channel_creation`` and a channel.
    """

    channel: Channel = Channel.from_dict(
        construct_client_dict(self, payload.data)
    )
    self.guilds[channel.guild_id].channels.append(channel)

    self.channels[channel.id] = channel

    return "on_channel_creation", channel


def export():
    return channel_create_middleware
