# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when the thread member object for the current user is updated"""

from ..core.dispatch import GatewayDispatch
from ..objects import ThreadMember
from ..utils import Timestamp
from ..utils.conversion import construct_client_dict


async def thread_member_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_thread_member_update``,
        creates a object for the thread member that is updated

    :param self:
        The current client.

    :param payload:
        The data received from the thread member update event.
    """
    return "on_thread_member_update", [
        ThreadMember.from_dict(construct_client_dict(
            self,
            {
                "join_timestamp": Timestamp(payload.data.pop("join_timestamp")),
                **payload.data
            }
        ))
    ]


def export():
    return thread_member_update_middleware
