# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild emoji is updated."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.guild import GuildEmojisUpdateEvent
from ..utils import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def guild_emojis_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_guild_emojis_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the guild emojis update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildEmojisUpdateEvent`]
        ``on_guild_emoji_update`` and a ``GuildEmojisUpdateEvent``
    """  # noqa: E501

    event = GuildEmojisUpdateEvent.from_dict(payload.data)
    guild = self.guild.get(event.guild_id)

    if guild:
        guild.emojis = event.emojis

    return ("on_guild_emojis_update", event)


def export() -> Coro:
    return guild_emojis_update_middleware
