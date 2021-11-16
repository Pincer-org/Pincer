# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is created in a subscribed text channel"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.message.user_message import UserMessage
from ..utils.conversion import construct_client_dict

if TYPE_CHECKING:
    from typing import List, Tuple

    from ..core.dispatch import GatewayDispatch


async def message_create_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[UserMessage]]:  # noqa: E501
    """|coro|

    Middleware for ``on_message`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.dispatch.GatewayDispatch`
        The data received from the message creation event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.message.user_message.UserMessage`]]
        ``on_message`` and a ``UserMessage``
    """  # noqa: E501
    return "on_message", [
        UserMessage.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return message_create_middleware
