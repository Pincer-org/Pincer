# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild emoji is updated."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildEmojisUpdateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_emojis_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_guild_emojis_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild emojis update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildEmojisUpdateEvent`]
        ``on_guild_emoji_update`` and a ``GuildEmojisUpdateEvent``
    """  # noqa: E501

    event = GuildEmojisUpdateEvent.from_dict(
        construct_client_dict(self, payload.data)
    )

    guild = self.guild.get(event.guild_id)
    if guild:
        guild.emojis = event.emojis

    return ("on_guild_emojis_update", event)


def export() -> Coro:
    return guild_emojis_update_middleware
