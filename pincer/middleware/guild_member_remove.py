# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a user is removed from a guild (leave/kick/ban).
"""

from ..core.dispatch import GatewayDispatch
from ..utils import Coro
from ..objects.events.guild import GuildMemberRemoveEvent


async def guild_member_remove(self, payload: GatewayDispatch):
    """
    Middleware for ``guild_member_remove`` event.

    :param self:
        The current client/bot.

    :param payload:
        The data received from the event.
    """

    return (
        "on_guild_member_remove",
        [GuildMemberRemoveEvent.from_dict(payload.data)]
    )


def export() -> Coro:
    return guild_member_remove
