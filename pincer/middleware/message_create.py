# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is created in a subscribed text channel"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.message.user_message import UserMessage

if TYPE_CHECKING:
    from typing import Tuple

    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_create_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
) -> Tuple[str, UserMessage]:  # noqa: E501
    """|coro|

    Middleware for the ``on_message`` event.

    Parameters
    ----------
    payload : :class:`pincer.core.gateway.GatewayDispatch`
        The data received from the message creation event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.message.user_message.UserMessage`]
        ``on_message`` and a ``UserMessage``
    """  # noqa: E501
    return ("on_message", UserMessage.from_dict(payload.data))


def export():
    return message_create_middleware
