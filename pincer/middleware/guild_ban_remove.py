# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild ban is removed."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildBanRemoveEvent
from ..utils import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_ban_remove_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_ban_remove`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild ban remove event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildBanRemoveEvent`]
        ``on_guild_ban_remove_update`` and a ``GuildBanRemoveEvent``
    """  # noqa: E501

    return ("on_guild_ban_remove", GuildBanRemoveEvent.from_dict(payload.data))


def export() -> Coro:
    return guild_ban_remove_middleware
