# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is deleted in a subscribed text channel"""

from ..core.dispatch import GatewayDispatch
from ..objects.events.message import MessageDeleteEvent
from ..utils.conversion import construct_client_dict


async def message_delete_middleware(self, payload: GatewayDispatch):
    """|coro|
    
    Middleware for ``on_message_delete`` event.

    Paramters
    ---------
    :param self:
        The current client.

    :param payload:
        The data received from the delete message event.
        
    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.events.message.MessageDeleteEvent`]
        ``on_message_delete`` and a ``MessageDeleteEvent`` object
    """
    return "on_message_delete", [
        MessageDeleteEvent.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return message_delete_middleware
