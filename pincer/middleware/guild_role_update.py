# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild role was updated."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildRoleUpdateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_role_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_role_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild role update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildRoleUpdateEvent`]]
        ``on_guild_role_update`` and a ``GuildRoleUpdateEvent``
    """

    return (
        "on_guild_role_update",
        [GuildRoleUpdateEvent.from_dict(construct_client_dict(self, payload.data))],
    )


def export() -> Coro:
    return guild_role_update_middleware
