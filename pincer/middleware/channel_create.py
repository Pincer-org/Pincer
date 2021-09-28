# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a channel is created/joined on the client"""
from pincer.core.dispatch import GatewayDispatch
from pincer.objects import Channel


def channel_create_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_error`` event.

    :param client:

    :param payload:
        The data received from the ready event.
    """

    return "on_channel_creation",  [
        Channel.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]
