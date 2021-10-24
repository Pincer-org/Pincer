# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a new user joins a guild. The inner payload is a guild member object
with an extra ``guild_id`` key.
"""

from ..core.dispatch import GatewayDispatch
from ..utils import Coro
from ..objects.events.guild import GuildMemberAddEvent


async def guild_member_add_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_guild_member_add`` event.

    :param self:
        The current client/bot.

    :param payload:
        The data received from the event.
    """

    return "on_guild_member_add", [GuildMemberAddEvent.from_dict(payload.data)]


def export() -> Coro:
    return guild_member_add_middleware
