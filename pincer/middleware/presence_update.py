# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.presence import PresenceUpdateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def presence_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_presence_update`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the presence update event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.user.voice_state.PresenceUpdateEvent`]]
        ``on_presence_update`` and a ``PresenceUpdateEvent``
    """
    return "on_presence_update", [
        PresenceUpdateEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return presence_update_middleware
