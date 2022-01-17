# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user explicitly removes all reactions from a message."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.message import MessageReactionRemoveAllEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_reaction_remove_all_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_message_reaction_remove_all`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the message reaction remove all event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageReactionRemoveAllEvent`]
        ``on_message_reaction_remove_all`` and an ``MessageReactionRemoveAllEvent``
    """  # noqa: E501

    return (
        "on_message_reaction_remove_all",
        MessageReactionRemoveAllEvent.from_dict(payload.data),
    )


def export():
    return message_reaction_remove_all_middleware
