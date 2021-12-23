# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user is updated"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.presence import PresenceUpdateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def presence_update_middleware(
    self: Client,
    gateway: Gateway,
    payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_presence_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the presence update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.user.voice_state.PresenceUpdateEvent`]
        ``on_presence_update`` and a ``PresenceUpdateEvent``
    """  # noqa: E501
    return (
        "on_presence_update",
        PresenceUpdateEvent.from_dict(construct_client_dict(self, payload.data)),
    )


def export() -> Coro:
    return presence_update_middleware
