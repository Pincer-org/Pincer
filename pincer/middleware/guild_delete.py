# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects.guild import UnavailableGuild
from ..utils.conversion import construct_client_dict


async def guild_delete_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_guild_delete``,
        creates a object for the guild that is deleted

    :param self:
        The current client.

    :param payload:
        The data received from the guild delete event.
    """
    return "on_guild_delete", [
        UnavailableGuild.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return guild_delete_middleware
