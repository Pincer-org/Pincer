# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when anyone is added to or removed from a thread"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.thread import ThreadMembersUpdateEvent
from ..utils.conversion import construct_client_dict


async def thread_members_update_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_thread_members_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the thread members update event.


    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.thread.ThreadMembersUpdateEvent`]
        ``on_thread_members_update`` and an ``ThreadMembersUpdateEvent``
    """  # noqa: E501
    return (
        "on_thread_members_update",
        ThreadMembersUpdateEvent.from_dict(
            construct_client_dict(self, payload.data)
        ),
    )


def export():
    return thread_members_update_middleware
