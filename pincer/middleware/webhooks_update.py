# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a user's voice state changes in a subscribed voice channel
(mute, volume, etc.)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.webhook import WebhooksUpdateEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def webhooks_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_webhooks_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the webhooks update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.webhook.WebhooksUpdateEvent`]
        ``on_webhooks_update`` and a ``WebhooksUpdateEvent``
    """  # noqa: E501
    return ("on_webhooks_update", WebhooksUpdateEvent.from_dict(payload.data))


def export():
    return webhooks_update_middleware
