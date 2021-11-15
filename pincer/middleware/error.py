# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent when there is an error,
including command responses
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..objects.events.error import DiscordError
from ..utils.conversion import construct_client_dict
from ..utils.types import Coro

if TYPE_CHECKING:
    from typing import List, Tuple
    from ..core.dispatch import GatewayDispatch


def error_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[DiscordError]]:
    """|coro|

    Middleware for ``on_error`` event.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the ready event.

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.events.error.DiscordError`]]
        ``"on_error"`` and a ``DiscordError``
    """
    # noqa: E501

    return "on_error", [
        DiscordError.from_dict(construct_client_dict(self, payload.data))
    ]


def export() -> Coro:
    return error_middleware
