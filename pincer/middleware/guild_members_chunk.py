# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent in response to Guild Request Members. You can use the ``chunk_index``
and ``chunk_count`` to calculate how many chunks are left for your request.
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildMembersChunkEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_member_chunk_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_member_chunk`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild member chunk event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildMemberChunkEvent`]]
        ``on_guild_member_chunk`` and a ``GuildMemberChunkEvent``
    """

    return (
        "on_guild_member_chunk",
        [GuildMembersChunkEvent.from_dict(
            construct_client_dict(self, payload.data)
        )]
    )


def export() -> Coro:
    return guild_member_chunk_middleware
