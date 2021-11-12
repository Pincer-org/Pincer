# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the user receives a Rich Presence Ask to Join request"""

from ..core.dispatch import GatewayDispatch
from ..objects.user.user import User
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


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


def export() -> Coro:
    return activity_join_request_middleware
