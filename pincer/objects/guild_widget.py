# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from typing import Optional

from ..utils import APIObject, Snowflake


@dataclass
class GuildWidget(APIObject):
    """
    Represents a Discord Guild Widget object

    :param enabled:
        whether the widget is enabled

    :param channel_id:
        the widget channel id
    """
    enabled: bool
    channel_id: Optional[Snowflake]
