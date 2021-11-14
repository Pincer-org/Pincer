# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild emoji is updated."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildEmojisUpdateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_emojis_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_emojis_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild emojis update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildEmojisUpdateEvent`]]
        ``on_guild_emoji_update`` and a ``GuildEmojisUpdateEvent``
    """

    return (
        "on_guild_emojis_update",
        [
            GuildEmojisUpdateEvent.from_dict(
                construct_client_dict(self, payload.data)
            )
        ],
    )


def export() -> Coro:
    return guild_emojis_update_middleware
