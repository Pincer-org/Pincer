# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent immediately after connecting,
contains server information
"""
from __future__ import annotations
from asyncio.tasks import ensure_future

from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from typing import Tuple
    from ..utils.types import Coro
    from ..client import Client
    from ..core.gateway import Dispatcher
    from ..core.dispatch import GatewayDispatch

_log = logging.getLogger(__package__)


async def on_resumed(
    self: Client,
    gateway: Dispatcher,
    payload: GatewayDispatch
) -> Tuple[str]:
    """|coro|

    Middleware for the ``on_resumed`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the stage instance create event

    Returns
    -------
    Tuple[:class:`str`]
        ``on_ready``
    """

    _log.debug(
        "%s Sucessfully reconnected to Discord gateway. Restarting heartbeat.",
        gateway.shard_key
    )
    gateway.start_heartbeat()

    return ("on_resumed",)


def export() -> Coro:
    return on_resumed
