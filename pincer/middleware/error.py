# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent when there is an error,
including command responses
"""
from ..core.dispatch import GatewayDispatch
from ..objects.events.error import DiscordError
from ..utils.conversion import construct_client_dict


def error_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_error`` event.

    :param self:
        The current client/bot.

    :param payload:
        The data received from the ready event.
    """

    return "on_error",  [
        DiscordError.from_dict(construct_client_dict(self, payload.data))
    ]
