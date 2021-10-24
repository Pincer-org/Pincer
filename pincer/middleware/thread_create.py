# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a thread is created/joined on the client."""

from ..core.dispatch import GatewayDispatch
from ..objects import Channel
from ..utils.conversion import construct_client_dict


def thread_create_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_thread_create`` event.

    :param self:
        The current client

    :param payload:
        The data received from the thread create event.
    """
    return "on_thread_create", [
        Channel.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return thread_create_middleware
