# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when an invite was created"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.invite import InviteCreateEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro


async def invite_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_invite_create``,

    Parameters
    ----------
    payload : :class:`GatewayDispatch`
        The data received from the invite create event

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.invite.InviteCreateEvent`]]
        ``on_invite_create`` and an ``InviteCreateEvent``
    """
    return "on_invite_create", [
        InviteCreateEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return invite_create_middleware
