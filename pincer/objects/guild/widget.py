# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Optional

    from ...utils.snowflake import Snowflake


@dataclass
class GuildWidget(APIObject):
    """Represents a Discord Guild Widget object

    Attributes
    ----------
    enabled: :class:`bool`
        Whether the widget is enabled
    channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The widget channel id
    """
    enabled: bool
    channel_id: Optional[Snowflake]
