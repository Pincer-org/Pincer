# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the client gains access to a channel"""

from __future__ import annotations

from typing import List

from ..core.dispatch import GatewayDispatch
from ..objects import Channel, ThreadMember
from ..objects.events.thread import ThreadListSyncEvent
from ..utils.conversion import construct_client_dict
from ..utils.types import JsonDict


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

    data: JsonDict = payload.data
    payload_members: List[JsonDict] = payload.data.pop("members")
    payload_threads: List[JsonDict] = payload.data.pop("threads")

    threads: List[Channel] = [
        Channel.from_dict(construct_client_dict(self, thread))
        for thread in payload_threads
    ]

    members: List[ThreadMember] = [
        ThreadMember.from_dict(construct_client_dict(self, member))
        for member in payload_members
    ]

    return (
        "on_thread_list_sync",
        ThreadListSyncEvent.from_dict(
            {"threads": threads, "members": members, **payload.data}
        )
    )


def export():
    return thread_list_sync
