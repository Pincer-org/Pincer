# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild role was updated."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildRoleUpdateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_role_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_guild_role_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild role update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildRoleUpdateEvent`]
        ``on_guild_role_update`` and a ``GuildRoleUpdateEvent``
    """

    event = GuildRoleUpdateEvent.from_dict(
        construct_client_dict(self, payload.data)
    )

    guild = self.guilds.get(event.guild_id)

    if guild:
        guild.roles = [
            role if role.id != event.role.id else event.role
            for role in guild.roles
        ]

    return ("on_guild_role_update", event)


def export() -> Coro:
    return guild_role_update_middleware
