# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

"""
non-subscription event sent when there is an error,
including command responses
"""
from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.dispatch import GatewayDispatch

from ..objects.events.error import DiscordError


def error_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[DiscordError]]:
    """Middleware for ``on_error`` event.

    Parameters
    ----------
    payload : GatewayDispatch
        The data received from the ready event.
    """
    return "on_error",  [
        DiscordError.from_dict(
            {"_client": self, "_http": self.http, **payload.data}
        )
    ]
