# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when anyone is added to or removed from a thread"""
from typing import List

from ..core.dispatch import GatewayDispatch
from ..objects import ThreadMember
from ..objects.events.thread import ThreadMembersUpdateEvent
from ..utils import Timestamp
from ..utils.conversion import construct_client_dict


async def thread_members_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_thread_member_update``,
        creates a object for the thread member that is updated

    :param self:
        The current client.

    :param payload:
        The data received from the thread member update event.
    """
    added_members: List[ThreadMember] = [
        ThreadMember.from_dict(construct_client_dict(
            self,
            {
                "join_timestamp": Timestamp(added_member.pop("join_timestamp")),
                **added_member
            }
        ))
        for added_member in payload.data.pop("added_members")
    ]

    return "on_thread_members_update", [
        ThreadMembersUpdateEvent.from_dict(
            {
                "added_members": added_members,
                **payload.data
            }
        )
    ]


def export():
    return thread_members_update_middleware
