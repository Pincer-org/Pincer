# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when multiple messages are deleted at once"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.message import MessageDeleteBulkEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_delete_bulk_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_message_delete_bulk`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the message delete bulk event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.message.MessageDeleteBulkEvent`]
        ``on_message_delete_bulk`` and an ``MessageDeleteBulkEvent``
    """
    return (
        "on_message_delete_bulk",
        MessageDeleteBulkEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return message_delete_bulk_middleware
