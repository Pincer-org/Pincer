# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when anyone is added to or removed from a thread"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.thread import ThreadMembersUpdateEvent

if TYPE_CHECKING:
    from ..client import Client
    from ..core.gateway import Gateway
    from ..core.gateway import GatewayDispatch


async def thread_members_update_middleware(
    self: Client, gateway: Gateway, payload: GatewayDispatch
):
    """|coro|

    Middleware for the ``on_thread_members_update`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.gateway.GatewayDispatch`
        The data received from the thread members update event.
    gateway : :class:`~pincer.core.gateway.Gateway`
        The gateway for the current shard.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.thread.ThreadMembersUpdateEvent`]
        ``on_thread_members_update`` and an ``ThreadMembersUpdateEvent``
    """  # noqa: E501
    return (
        "on_thread_members_update",
        ThreadMembersUpdateEvent.from_dict(payload.data),
    )


def export():
    return thread_members_update_middleware
