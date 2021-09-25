# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from pincer.utils.api_object import APIObject
from pincer.utils.snowflake import Snowflake


@dataclass
class WebhookUpdateEvent(APIObject):
    """
    Sent when a guild's channel webhook
    is created, updated, or deleted.

    :param guild_id:
        id of the guild

    :param channel_id:
        id of the channel
    """
    guild_id: Snowflake
    channel_id: Snowflake
