# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a user explicitly removes all reactions from a message."""

from ..core.dispatch import GatewayDispatch
from ..objects.events.message import MessageReactionRemoveAllEvent
from ..utils.conversion import construct_client_dict


async def message_reaction_remove_all_middleware(
    self,
    payload: GatewayDispatch):
    """
    Middleware for ``on_message_reaction_remove_all``,
        creates a object for the message reactions that are removed

    :param self:
        The current client.

    :param payload:
        The data received from the message reaction remove all event.
    """
    return "on_message_reaction_remove_all", [
        MessageReactionRemoveAllEvent.from_dict(
            construct_client_dict(self, payload.data)
        )
    ]


def export():
    return message_reaction_remove_all_middleware
