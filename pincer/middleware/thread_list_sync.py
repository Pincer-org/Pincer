# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client gains access to a channel"""

from __future__ import annotations

from typing import List

from ..core.dispatch import GatewayDispatch
from ..objects.events.thread import ThreadListSyncEvent
from ..utils.conversion import construct_client_dict


async def thread_list_sync(self, payload: GatewayDispatch):
    """|coro|

    Middleware for the ``on_thread_list_sync`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the thread list sync event.

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.guild.events.thread.ThreadListSyncEvent`]
        ``on_thread_list_sync`` and an ``ThreadListSyncEvent``
    """  # noqa: E501

    event = ThreadListSyncEvent.from_dict(
        construct_client_dict(self, payload.data)
    )

    guild = self.guilds.get(event.guild_id)
    if guild:
        guild.threads = event.threads

    return "on_thread_list_sync", event


def export():
    return thread_list_sync
