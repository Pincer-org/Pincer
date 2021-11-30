# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild role was deleted."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.guild import GuildRoleDeleteEvent
from ..utils import Coro
from ..utils.conversion import construct_client_dict


async def guild_role_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_guild_role_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the guild role delete event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.guild.GuildRoleDeleteEvent`]
        ``on_guild_role_delete`` and a ``GuildRoleDeleteEvent``
    """  # noqa: E501

    return (
        "on_guild_role_delete",
        GuildRoleDeleteEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return guild_role_delete_middleware
