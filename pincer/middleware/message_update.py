# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is updated in a subscribed text channel"""

from ..core.dispatch import GatewayDispatch
from ..objects import UserMessage
from ..utils.conversion import construct_client_dict


async def message_update_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_message_update`` event,
        generate a class for the message that has been updated.

    :param self:
        The current client.

    :param payload:
        The data received from the message update event.

    """
    return "on_message_update", [
        UserMessage.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return message_update_middleware
