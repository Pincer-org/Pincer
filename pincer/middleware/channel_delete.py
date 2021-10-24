# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a channel is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


async def channel_delete_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_channel_delete``,
        creates a object for the channel that is deleted

    :param self:
        The current client.

    :param payload:
        The data received from the channel delete event.
    """
    return "on_channel_delete", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return channel_delete_middleware
