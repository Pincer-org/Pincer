# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an invite is deleted"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.invite import InviteDeleteEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def invite_delete_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_invite_delete``,

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the invite delete event

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.events.invite.InviteDeleteEvent`]]
        ``on_invite_delete`` and an ``InviteDeleteEvent``
    """
    return "on_invite_delete", [
        InviteDeleteEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return invite_delete_middleware
