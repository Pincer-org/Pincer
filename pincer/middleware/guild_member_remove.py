# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a user is removed from a guild (leave/kick/ban).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildMemberRemoveEvent
from ..utils import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_member_remove_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_member_remove`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild member remove event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildMemberRemoveEvent`]
        ``on_guild_member_remove`` and a ``GuildMemberRemoveEvent``
    """

    return (
        "on_guild_member_remove",
        GuildMemberRemoveEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return guild_member_remove_middleware
