# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a guild member is updated. This will also fire when the user object
of a guild member changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildMemberUpdateEvent
from ..utils import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_member_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_member_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild member update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildMemberUpdateEvent`]
        ``on_guild_member_update`` and a ``GuildMemberUpdateEvent``
    """

    return (
        "on_guild_member_update",
        GuildMemberUpdateEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return guild_member_update_middleware
