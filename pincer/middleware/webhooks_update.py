# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.webhook import WebhooksUpdateEvent
from ..utils.conversion import construct_client_dict


async def webhooks_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_webhooks_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the webhooks update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.webhook.WebhooksUpdateEvent`]
        ``on_webhooks_update`` and a ``WebhooksUpdateEvent``
    """  # noqa: E501
    return (
        "on_webhooks_update",
        WebhooksUpdateEvent.from_dict(construct_client_dict(self, payload.data)),
    )


def export():
    return webhooks_update_middleware
