# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an integration is deleted"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.integration import IntegrationDeleteEvent
from ..utils.types import Coro

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def integration_delete_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_integration_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the integration delete event
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.integration.IntegrationDeleteEvent`]
        ``on_integration_delete`` and an ``IntegrationDeleteEvent``
    """  # noqa: E501
    return (
        "on_integration_delete",
        IntegrationDeleteEvent.from_dict(payload.data),
    )


def export() -> Coro:
    return integration_delete_middleware
