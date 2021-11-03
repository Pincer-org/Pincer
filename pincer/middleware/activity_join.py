# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when the user clicks a Rich Presence join invite in chat
to join a game.
"""

from pincer.objects.events.activity import ActivityJoinEvent
from pincer.utils.conversion import construct_client_dict
from ..core.dispatch import GatewayDispatch
from ..utils.types import Coro


async def activity_join_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_activity_join`` event.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot.

    payload : :class:`GatewayDispatch`
        The data received from the activity join event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`ActivityJoinEvent`]]
        ``on_activity_join`` and an ``ActivityJoinEvent`` object
    """
    return "on_activity_join", [
        ActivityJoinEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return activity_join_middleware
