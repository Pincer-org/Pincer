# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING, APINullable

if TYPE_CHECKING:
    from ...utils.snowflake import Snowflake


class IntegrationDeleteEvent(APIObject):
    """Sent when an integration is deleted.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        integration id
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        id of the guild
    application_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        id of the bot/OAuth2 application for this discord integration
    """

    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake] = MISSING


class IntegrationCreateEvent(APIObject):
    """
    Sent when an integration is created.

    Attributes
    ----------
    id : :class:`Snowflake`
        integration id

    guild_id : :class:`Snowflake`
        id of the guild

    application_id : APINullable[:class:`Snowflake`]
        id of the bot/OAuth2 application for this discord integration
    """

    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake] = MISSING


class IntegrationUpdateEvent(APIObject):
    """
    Sent when an integration is updated.

    Attributes
    ----------
    id : :class:`Snowflake`
        integration id

    guild_id : :class:`Snowflake`
        id of the guild

    application_id : APINullable[:class:`Snowflake`]
        id of the bot/OAuth2 application for this discord integration
    """

    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake] = MISSING
