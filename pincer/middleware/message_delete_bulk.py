# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when multiple messages are deleted at once"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.message import MessageDeleteBulkEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def message_delete_bulk_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_message_delete_bulk`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the message delete bulk event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.message.MessageDeleteBulkEvent`]
        ``on_message_delete_bulk`` and an ``MessageDeleteBulkEvent``
    """
    return (
        "on_message_delete_bulk",
        MessageDeleteBulkEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return message_delete_bulk_middleware
