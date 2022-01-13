# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when the user clicks a Rich Presence join invite in chat
to join a game.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.activity import ActivityJoinEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def activity_join_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_activity_join`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the activity join event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.activity.ActivityJoinEvent`]
        ``on_activity_join`` and an ``ActivityJoinEvent``
    """  # noqa: E501
    return (
        "on_activity_join",
        ActivityJoinEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return activity_join_middleware
