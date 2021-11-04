# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING, APINullable


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


@dataclass
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


@dataclass
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
