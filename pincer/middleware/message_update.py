# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is updated in a subscribed text channel"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import UserMessage

if TYPE_CHECKING:
    from typing import Tuple

    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
) -> Tuple[str, UserMessage]:
    """|coro|


    Middleware for the ``on_message_update`` event.
        generate a class for the message that has been updated.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the message update event event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.message.user_message.UserMessage`]
        ``on_message_update`` and a ``UserMessage``
    """  # noqa: E501
    return ("on_message_update", UserMessage.from_dict(payload.data))


def export():
    return message_update_middleware
