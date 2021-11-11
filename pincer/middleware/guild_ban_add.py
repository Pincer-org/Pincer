# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild ban is add."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildBanAddEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_ban_add_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_ban_add`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild ban add event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildBaAddEvent`]]
        ``on_guild_ban_add_update`` and a ``GuildBanAddEvent``
    """

    return (
        "on_guild_ban_add",
        [GuildBanAddEvent.from_dict(construct_client_dict(self, payload.data))],
    )


def export() -> Coro:
    return guild_ban_add_middleware
