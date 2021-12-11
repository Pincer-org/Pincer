# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an integration is created"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.integration import IntegrationCreateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def integration_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_integration_create`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the integration create event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.integration.IntegrationCreateEvent`]
        ``on_integration_create`` and an ``IntegrationCreateEvent``
    """  # noqa: E501
    return (
        "on_integration_create",
        IntegrationCreateEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return integration_create_middleware
