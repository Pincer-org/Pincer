# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when a new user joins a guild. The inner payload is a guild member object
with an extra ``guild_id`` key.
"""

from ..core.dispatch import GatewayDispatch
from ..utils import Coro
from ..utils.conversion import construct_client_dict
from ..objects.events.guild import GuildMemberAddEvent


async def guild_member_add_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_add`` event.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.

    payload : :class:`GatewayDispatch`
        The data received from the guild member add event.
    """

    return "on_guild_member_add", [
        GuildMemberAddEvent.from_dict(
            construct_client_dict(self, payload.data)
        )
    ]


def export() -> Coro:
    return guild_member_add_middleware
