# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is created/joined on the client"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.guild import Guild
from ..utils.conversion import construct_client_dict

if TYPE_CHECKING:
    from typing import List, Tuple
    from ..core.dispatch import GatewayDispatch


async def guild_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_create``,
        generate the guild class that was created

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild create event

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.Guild`]]

        ``on_guild_create`` and a ``Guild``
    """
    guild = Guild.from_dict(construct_client_dict(self, payload.data))
    self.guilds[guild.id] = guild
    return "on_guild_create", [guild]


def export():
    return guild_create_middleware
