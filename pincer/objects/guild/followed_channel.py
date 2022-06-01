# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject, ChannelProperty

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


@dataclass(repr=False)
class FollowedChannel(APIObject, ChannelProperty):
    """Represents a Discord Followed Channel object

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        Source channel id
    webhook_id: :class:`~pincer.utils.snowflake.Snowflake`
        Created target webhook id
    """

    channel_id: Snowflake
    webhook_id: Snowflake
