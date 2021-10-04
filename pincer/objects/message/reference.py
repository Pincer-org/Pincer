# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils import APINullable, Snowflake


@dataclass
class MessageReference(APIObject):
    """
    Represents a Discord Message Reference object

    :param message_id:
        id of the originating message

    :param channel_id:
        id of the originating message's channel

    :param guild_id:
        id of the originating message's guild

    :param fail_if_not_exists:
        when sending, whether to error if the referenced message doesn't
        exist instead of sending as a normal (non-reply) message,
        default true
    """
    message_id: APINullable[Snowflake] = MISSING
    channel_id: APINullable[Snowflake] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    fail_if_not_exists: APINullable[bool] = True
