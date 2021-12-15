# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when the client receives a notification
(mention or new message in eligible channels)
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.notification import NotificationCreateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def notification_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_notification_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the notification create event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.notification.NotificationCreateEvent`]
        ``on_notification_create`` and a ``NotificationCreateEvent``
    """  # noqa: E501
    channel_id = payload.data.get("channel_id")
    payload.data["message"]["channel_id"] = channel_id
    return (
        "on_notification_create",
        NotificationCreateEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return notification_create_middleware
