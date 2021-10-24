# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a guild member is updated. This will also fire when the user object
of a guild member changes.
"""

from ..core.dispatch import GatewayDispatch
from ..utils import Coro
from ..utils.conversion import construct_client_dict
from ..objects.events.guild import GuildMemberUpdateEvent


async def guild_member_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_guild_member_update`` event.

    :param self:
        The current client/bot.

    :param payload:
        The data received from the event.
    """

    return (
        "on_guild_member_update",
        [GuildMemberUpdateEvent.from_dict(
            construct_client_dict(self, payload.data)
        )]
    )


def export() -> Coro:
    return guild_member_update_middleware
