# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when the client receives a notification
(mention or new message in eligible channels)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.notification import NotificationCreateEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def notification_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_notification_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the notification create event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.notification.NotificationCreateEvent`]
        ``on_notification_create`` and a ``NotificationCreateEvent``
    """  # noqa: E501
    channel_id = payload.data.get("channel_id")
    payload.data["message"]["channel_id"] = channel_id
    return (
        "on_notification_create",
        NotificationCreateEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return notification_create_middleware
