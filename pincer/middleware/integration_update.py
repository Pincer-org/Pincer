# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an integration is updated"""

from pincer.utils.types import Coro
from ..core.dispatch import GatewayDispatch
from ..objects.events.integration import IntegrationUpdateEvent
from ..utils.conversion import construct_client_dict


async def integration_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_integration_update``,

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot

    payload : :class:`GatewayDispatch`
        The data recieved from the integration update event

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.events.integration.IntegrationUpdateEvent`]]
        ``on_integration_update`` and an ``IntegrationUpdateEvent`` object
    """
    return "on_integration_update", [
        IntegrationUpdateEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return integration_update_middleware
