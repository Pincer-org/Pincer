# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user started typing in a channel"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.typing_start import TypingStartEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def typing_start_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_typing_start`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the typing start event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.typing_start.TypingStartEvent`]
        ``on_typing_start`` and a ``TypingStartEvent``
    """  # noqa: E501
    return ("on_typing_start", TypingStartEvent.from_dict(payload.data))


def export() -> Coro:
    return typing_start_middleware
