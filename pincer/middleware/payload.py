# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple

    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def payload_middleware(
    self: Client,
    gateway: Gateway,
    payload: GatewayDispatch,
) -> Tuple[str, GatewayDispatch]:
    """Invoked when anything is received from gateway.


    Parameters
    ----------
    payload : :class:`pincer.core.gateway.GatewayDispatch`
        The data received from the ready event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.core.gateway.GatewayDispatch`]
        ``on_payload`` and a ``payload``
    """
    return "on_payload", payload


def export():
    return payload_middleware
