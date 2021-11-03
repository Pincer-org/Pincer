# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""sent when a message is created in a subscribed text channel"""

from ..core.dispatch import GatewayDispatch
from ..objects import UserMessage
from ..utils.conversion import construct_client_dict


async def message_create_middleware(self, payload: GatewayDispatch):
    """|coro|

    Middleware for ``on_message`` event,
        generate a class for the message that has been created.

    Parameters
    ----------
    self : :class:`Client`
        The current client/bot

    payload : :class:`GatewayDispatch`
        The data recieved from the message create event

    Returns
    -------
    Tuple[:class:`str`, :class:`~pincer.objects.message.user_message.UserMessage`]
        ``on_message`` and a ``UserMessage``
    """
    return "on_message", [
        UserMessage.from_dict(construct_client_dict(self, payload.data))
    ]


def export():
    return message_create_middleware
