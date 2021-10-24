# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a guild is updated"""
from typing import List

from ..core.dispatch import GatewayDispatch
from ..objects import Guild, Channel
from ..utils.conversion import construct_client_dict


async def guild_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_guild_update``,
        creates a object for the guild that is updated

    :param self:
        The current client.

    :param payload:
        The data received from the guild update event.
    """
    channel_list = payload.data.pop("channels", [])

    channels: List[Channel] = [
        Channel.from_dict(construct_client_dict(self, channel))
        for channel in channel_list
    ]

    return "on_guild_update", [
        Guild.from_dict(construct_client_dict(
            self,
            {"channels": channels, **payload.data}
        ))
    ]


def export():
    return guild_update_middleware
