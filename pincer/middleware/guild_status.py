# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""Event sent when a subscribed server's state changes"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildStatusEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_status_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_status`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild status event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Return
    ------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildStatusEvent`]
        ``on_guild_status`` and a ``GuildStatusEvent``
    """
    return ("on_guild_status", GuildStatusEvent.from_dict(payload.data))


def export() -> Coro:
    return guild_status_middleware
