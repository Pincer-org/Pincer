# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


@dataclass
class MessageReference(APIObject):
    """Represents a Discord Message Reference object

    Attributes
    ----------
    message_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the originating message
    channel_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the originating message's channel
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the originating message's guild
    fail_if_not_exists: APINullable[:class:`bool`]
        When sending, whether to error if the referenced message doesn't
        exist instead of sending as a normal (non-reply) message,
        default true
    """
    message_id: APINullable[Snowflake] = MISSING
    channel_id: APINullable[Snowflake] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    fail_if_not_exists: APINullable[bool] = True
