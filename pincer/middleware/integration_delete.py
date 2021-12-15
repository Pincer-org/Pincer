# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an integration is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.integration import IntegrationDeleteEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def integration_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_integration_delete`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the integration delete event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.events.integration.IntegrationDeleteEvent`]
        ``on_integration_delete`` and an ``IntegrationDeleteEvent``
    """  # noqa: E501
    return (
        "on_integration_delete",
        IntegrationDeleteEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export() -> Coro:
    return integration_delete_middleware
