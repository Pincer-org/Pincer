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
