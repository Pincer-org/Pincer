# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild ban is removed."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildBanRemoveEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_ban_remove_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_ban_remove`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild ban remove event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildBanRemoveEvent`]]
        ``on_guild_ban_remove_update`` and a ``GuildBanRemoveEvent``
    """

    return (
        "on_guild_ban_remove",
        [GuildBanRemoveEvent.from_dict(construct_client_dict(self, payload.data))],
    )


def export() -> Coro:
    return guild_ban_remove_middleware
