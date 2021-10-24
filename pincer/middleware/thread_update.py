# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


async def thread_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_thread_update``,
        creates a object for the thread that is updated

    :param self:
        The current client.

    :param payload:
        The data received from the thread update event.
    """
    return "on_thread_update", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return thread_update_middleware
