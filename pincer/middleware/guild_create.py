# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is created/joined on the client"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..objects.guild import Guild
    from ..core.dispatch import GatewayDispatch
    from ..utils.conversion import construct_client_dict


def guild_create_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[Guild]]:
    """|coro|

    Middleware for ``on_guild_create`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.guild.guild.Guild`]]
        ``on_guild_create`` and a ``Guild``
    """
    return "on_guild_create", [
        Guild.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return guild_create_middleware
