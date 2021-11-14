# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
Activitys
"""

from ..objects.events.activity import ActivitySpectateEvent, ActivityJoinEvent
from ..utils.conversion import construct_client_dict
from ..core.dispatch import GatewayDispatch
from ..utils.types import Coro
from ..objects.user.user import User


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


async def activity_join_request_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_activity_join_request`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the activity join request event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.user.user.User`]]
        ``on_activity_join_request`` and a ``User``
    """
    return "on_activity_join_request", [
        User.from_dict(construct_client_dict(self, payload.data))
    ]


async def activity_join_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_activity_join`` event.

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the activity join event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`ActivityJoinEvent`]]
        ``on_activity_join`` and an ``ActivityJoinEvent``
    """
    return "on_activity_join", [
        ActivityJoinEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return (
        activity_spectate_middleware,
        activity_join_middleware,
        activity_join_request_middleware,
    )
