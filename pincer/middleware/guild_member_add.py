# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a new user joins a guild. The inner payload is a guild member object
with an extra ``guild_id`` key.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildMemberAddEvent
from ..utils import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_member_add_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_member_add`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild member add event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildMemberAddEvent`]
        ``on_guild_member_add`` and a ``GuildMemberAddEvent``
    """

    return ("on_guild_member_add", GuildMemberAddEvent.from_dict(payload.data))


def export() -> Coro:
    return guild_member_add_middleware
