# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a user is removed from a guild (leave/kick/ban).
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildMemberRemoveEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_member_remove_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_remove`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild member remove event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildMemberRemoveEvent`]]
        ``on_guild_member_remove`` and a ``GuildMemberRemoveEvent``
    """

    return (
        "on_guild_member_remove",
        [GuildMemberRemoveEvent.from_dict(construct_client_dict(self, payload.data))],
    )


def export() -> Coro:
    return guild_member_remove_middleware
