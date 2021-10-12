# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Optional

    from ...utils.snowflake import Snowflake


@dataclass
class VoiceServerUpdateEvent(APIObject):
    """
    Sent when a guild's voice server is updated.
    This is sent when initially connecting to voice,
    and when the current voice instance fails over to a new server.

    :param token:
        voice connection token

    :param guild_id:
        the guild this voice server update is for

    :param endpoint:
        the voice server host
    """
    token: str
    guild_id: Snowflake
    endpoint: Optional[str] = None
