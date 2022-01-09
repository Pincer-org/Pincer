# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user removes a reaction to a message"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Emoji
from ..objects.events.message import MessageReactionRemoveEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_reaction_remove_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_message_reaction_remove`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the message reaction remove event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageReactionRemoveEvent`]
        ``on_message_reaction_remove`` and an ``MessageReactionRemoveEvent``
    """  # noqa: E501

    return (
        "on_message_reaction_remove",
        MessageReactionRemoveEvent.from_dict(
            {
                "emoji": Emoji.from_dict(payload.data.pop("emoji")),
                **payload.data,
            }
        ),
    )


def export():
    return message_reaction_remove_middleware
