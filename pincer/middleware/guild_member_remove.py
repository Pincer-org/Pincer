# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a user is removed from a guild (leave/kick/ban).
"""

from ..core.dispatch import GatewayDispatch
from ..utils import Coro
from ..utils.conversion import construct_client_dict
from ..objects.events.guild import GuildMemberRemoveEvent


async def guild_member_remove_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_remove`` event.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.

    payload : :class:`GatewayDispatch`
        The data received from the guild member remove event.
    """

    return (
        "on_guild_member_remove",
        [GuildMemberRemoveEvent.from_dict(
            construct_client_dict(self, payload.data)
        )]
    )


def export() -> Coro:
    return guild_member_remove_middleware
