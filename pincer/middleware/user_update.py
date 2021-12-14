# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when properties about a user changes"""

from ..core.dispatch import GatewayDispatch
from ..objects.user import User
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def user_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_user_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the user update event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.user.user.User`]
        ``on_user_update`` and a ``User``
    """
    return (
        "on_user_update",
        User.from_dict(construct_client_dict(self, payload.data)),
    )


def export() -> Coro:
    return user_update_middleware
