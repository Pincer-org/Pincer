# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild sticker is updated."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildStickersUpdateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_stickers_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_guild_stickers_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild stickers update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildStickersUpdateEvent`]
        ``on_guild_sticker_update`` and a ``GuildStickersUpdateEvent``
    """  # noqa: E501

    event = GuildStickersUpdateEvent.from_dict(
        construct_client_dict(self, payload.data)
    )

    guild = self.guilds.get(event.guild_id)

    if guild:
        guild.stickers = event.stickers

    return ("on_guild_stickers_update", event)


def export() -> Coro:
    return guild_stickers_update_middleware
