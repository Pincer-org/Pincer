# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.webhook import WebhookUpdateEvent
from ..utils.conversion import construct_client_dict


async def webhook_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_webhook_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the webhooks update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.webhook.WebhookUpdateEvent`]]
        ``on_webhook_update`` and a ``WebhookUpdateEvent``
    """
    return "on_webhook_update", [
        WebhookUpdateEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return webhook_update_middleware
