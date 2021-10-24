# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


async def thread_delete_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_thread_delete``,
        creates a object for the thread that is deleted

    :param self:
        The current client.

    :param payload:
        The data received from the thread delete event.
    """
    return "on_thread_delete", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return thread_delete_middleware
