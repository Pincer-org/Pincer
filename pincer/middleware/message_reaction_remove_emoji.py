# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when a bot removes all instances of a given emoji from the reactions of a message
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import Emoji
from ..objects.events.message import MessageReactionRemoveEmojiEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_reaction_remove_emoji_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_message_reaction_remove_emoji`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the message reaction remove emoji event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageReactionRemoveEmojiEvent`]
        ``on_message_reaction_remove_emoji`` and an ``MessageReactionRemoveEmojiEvent``
    """  # noqa: E501

    return (
        "on_message_reaction_remove_emoji",
        MessageReactionRemoveEmojiEvent.from_dict(
            {
                "emoji": Emoji.from_dict(payload.data.pop("emoji")),
                **payload.data,
            }
        ),
    )


def export():
    return message_reaction_remove_emoji_middleware
