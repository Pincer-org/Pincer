# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild sticker is updated."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildStickersUpdateEvent
from ..utils import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_stickers_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_stickers_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild stickers update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildStickersUpdateEvent`]
        ``on_guild_sticker_update`` and a ``GuildStickersUpdateEvent``
    """  # noqa: E501

    event = GuildStickersUpdateEvent.from_dict(payload.data)
    guild = self.guilds.get(event.guild_id)

    if guild:
        guild.stickers = event.stickers

    return ("on_guild_stickers_update", event)


def export() -> Coro:
    return guild_stickers_update_middleware
