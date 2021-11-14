# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


@dataclass
class WebhooksUpdateEvent(APIObject):
    """
    Sent when a guild's channel webhook
    is created, updated, or deleted.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        id of the guild
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        id of the channel
    """
    guild_id: Snowflake
    channel_id: Snowflake
