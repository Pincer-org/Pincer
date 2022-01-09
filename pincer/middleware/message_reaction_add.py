# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user adds a reaction to a message"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects import GuildMember, Emoji
from ..objects.events.message import MessageReactionAddEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def message_reaction_add_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_message_reaction_add`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the message reaction add event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageReactionAddEvent`]
        ``on_message_reaction_add`` and an ``MessageReactionAddEvent``
    """  # noqa: E501

    return (
        "on_message_reaction_add",
        MessageReactionAddEvent.from_dict(
            {
                "member": GuildMember.from_dict(payload.data.pop("member")),
                "emoji": Emoji.from_dict(payload.data.pop("emoji")),
                **payload.data,
            }
        ),
    )


def export():
    return message_reaction_add_middleware
