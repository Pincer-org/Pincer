# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild role was created."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildRoleCreateEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_role_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_guild_role_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild role create event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildRoleCreateEvent`]
        ``on_guild_role_create`` and a ``GuildRoleCreateEvent``
    """  # noqa: E501

    event = GuildRoleCreateEvent.from_dict(
        construct_client_dict(self, payload.data)
    )

    guild = self.guilds.get(event.guild_id)
    if guild:
        guild.roles.append(event.role)

    return ("on_guild_role_create", event)


def export() -> Coro:
    return guild_role_create_middleware
