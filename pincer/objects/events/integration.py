# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

from ...utils.api_object import APIObject
from ...utils.types import MISSING, APINullable

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


@dataclass
class IntegrationDeleteEvent(APIObject):
    """
    Sent when an integration is deleted.

    :param id:
        integration id

    :param guild_id:
        id of the guild

    :param application_id:
        id of the bot/OAuth2 application for this discord integration
    """
    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake] = MISSING
