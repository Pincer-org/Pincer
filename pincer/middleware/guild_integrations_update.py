# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild integration is updated."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildIntegrationsUpdateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_integrations_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_integrations_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the guild integrations update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.guild.GuildIntegrationsUpdateEvent`]]
        ``on_guild_integration_update`` and a ``GuildIntegrationsUpdateEvent``
    """

    return (
        "on_guild_integrations_update",
        [
            GuildIntegrationsUpdateEvent.from_dict(
                construct_client_dict(self, payload.data)
            )
        ],
    )


def export() -> Coro:
    return guild_integrations_update_middleware
