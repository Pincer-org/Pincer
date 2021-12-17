# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Sent when the user clicks a Rich Presence join invite in chat
to join a game.
"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.activity import ActivityJoinEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def activity_join_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_activity_join`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the activity join event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.activity.ActivityJoinEvent`]
        ``on_activity_join`` and an ``ActivityJoinEvent``
    """  # noqa: E501
    return (
        "on_activity_join",
        ActivityJoinEvent.from_dict(construct_client_dict(self, payload.data)),
    )


def export() -> Coro:
    return activity_join_middleware
