# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is deleted in a subscribed text channel"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.message import MessageDeleteEvent
from ..utils.conversion import construct_client_dict

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..core.dispatch import GatewayDispatch


async def on_message_delete_middleware(
    self, payload: GatewayDispatch
) -> Tuple[str, MessageDeleteEvent]:
    """|coro|
    Middleware for the ``on_message_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the message delete event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageDeleteEvent`]
        ``on_message_delete`` and a ``MessageDeleteEvent``
    """  # noqa: E501

    return (
        "on_message_delete",
        MessageDeleteEvent.from_dict(construct_client_dict(self, payload.data)),
    )


def export():
    return on_message_delete_middleware
