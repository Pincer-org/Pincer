# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass

from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake


@dataclass
class FollowedChannel(APIObject):
    """Represents a Discord Followed Channel object

    :param channel_id:
        source channel id

    :param webhook_id:
        created target webhook id
    """
    channel_id: Snowflake
    webhook_id: Snowflake
