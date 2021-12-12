# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild role was deleted."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildRoleDeleteEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_role_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_guild_role_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild role delete event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildRoleDeleteEvent`]
        ``on_guild_role_delete`` and a ``GuildRoleDeleteEvent``
    """  # noqa: E501

    event = GuildRoleDeleteEvent.from_dict(
        construct_client_dict(self, payload.data)
    )

    guild = self.guilds.get(event.guild_id)

    if guild:
        guild.roles = [
            role for role in self.guilds[event.guild_id].roles
            if role.id != event.role_id
        ]

    return ("on_guild_role_delete", event)


def export() -> Coro:
    return guild_role_delete_middleware
