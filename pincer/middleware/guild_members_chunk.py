# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent in response to Guild Request Members. You can use the ``chunk_index``
and ``chunk_count`` to calculate how many chunks are left for your request.
"""

from ..core.dispatch import GatewayDispatch
from ..utils import Coro
from ..objects.events.guild import GuildMembersChunkEvent


async def guild_member_chunk_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_guild_member_chunk`` event.

    :param self:
        The current client/bot.

    :param payload:
        The data received from the event.
    """

    return (
        "on_guild_member_chunk",
        [GuildMembersChunkEvent.from_dict(payload.data)]
    )


def export() -> Coro:
    return guild_member_chunk_middleware
