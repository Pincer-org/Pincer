# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an integration is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.integration import IntegrationUpdateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def integration_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_integration_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the integration update event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.integration.IntegrationUpdateEvent`]
        ``on_integration_update`` and an ``IntegrationUpdateEvent``
    """  # noqa: E501
    return (
        "on_integration_update",
        IntegrationUpdateEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return integration_update_middleware
