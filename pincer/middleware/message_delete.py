# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is deleted in a subscribed text channel"""
from __future__ import annotations

from typing import List, Tuple

from ..core.dispatch import GatewayDispatch
from ..objects.events.message import MessageDeleteEvent


async def on_message_delete_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[MessageDeleteEvent]]:
    """|coro|

    Middleware for ``?`` event. # TODO ``?`` here because idk what it is

    Parameters
    ----------
    payload : :class:¬pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.message.MessageDeleteEvent`]]
        ``on_message_delete`` and a ``MessageDeleteEvent``
    """
    return "on_message_delete", [
        MessageDeleteEvent.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]


def export():
    return on_message_delete_middleware
