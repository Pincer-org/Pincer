# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an invite is deleted"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.invite import InviteDeleteEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def invite_delete_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_invite_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the invite delete event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.invite.InviteDeleteEvent`]
        ``on_invite_delete`` and an ``InviteDeleteEvent``
    """
    return ("on_invite_delete", InviteDeleteEvent.from_dict(payload.data))


def export() -> Coro:
    return invite_delete_middleware
