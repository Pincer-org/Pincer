# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
sent when the user clicks a Rich Presence spectate invite in chat to
spectate a game
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.activity import ActivitySpectateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def activity_spectate_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_activity_spectate`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the activity spectate event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`ActivitySpectateEvent`]]
        ``on_activity_spectate`` and an ``ActivitySpectateEvent``
    """
    return "on_activity_spectate", [
        ActivitySpectateEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return activity_spectate_middleware
