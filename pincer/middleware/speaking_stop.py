# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user in a subscribed voice channel stops speaking"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.voice import SpeakingStopEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def speaking_stop_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_speaking_stop`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the speaking stop event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`Snowflake`]
        ``on_speaking_stop`` and a ``Snowflake`` (user_id)
    """
    return ("on_speaking_stop", SpeakingStopEvent.from_dict(payload.data))


def export() -> Coro:
    return speaking_stop_middleware
