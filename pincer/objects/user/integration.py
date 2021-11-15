# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from .user import User
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp


class IntegrationExpireBehavior(IntEnum):
    """Represents a Discord Integration expire behavior

    Attributes
    ----------
    REMOVE_ROLE:
        Remove role on expire.
    KICK:
        Kick on expire.
    """
    REMOVE_ROLE = 0
    KICK = 1


@dataclass
class IntegrationAccount(APIObject):
    """Represents a Discord Integration Account object

    Attributes
    ----------
    id: :class:`str`
        Id of the account
    name: :class:`str`
        Name of the account
    """
    id: str
    name: str


@dataclass
class IntegrationApplication(APIObject):
    """Represents a Discord Integration Application object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the app
    name: :class:`str`
        The name of the app
    icon: Optional[:class:`str`]
        The icon hash of the app
    description: :class:`str`
        The description of the app
    summary: :class:`str`
        The summary of the app
    bot: APINullable[:class:`~pincer.objects.user.user.User`]
        The bot associated with this application
    """
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    summary: str
    bot: APINullable[User] = MISSING


@dataclass
class Integration(APIObject):
    """Represents a Discord Integration object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Integration id
    name: :class:`str`
        Integration name
    type: :class:`str`
        Integration type (twitch, youtube, or discord)$
    enabled: :class:`bool`
        Is this integration enabled
    account: :class:`~pincer.objects.user.integration.IntegrationAccount`
        Integration account information
    syncing: APINullable[:class:`bool`]
        Is this integration syncing
    role_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id that this integration uses for subscribers
    enable_emoticons: APINullable[:class:`bool`]
        Whether emoticons should be synced for this integration
        (twitch only currently)
    expire_behavior: APINullable[:class:`~pincer.objects.user.integration.IntegrationExpireBehavior`]
        The behavior of expiring subscribers
    expire_grace_period: APINullable[:class:`int`]
        The grace period (in days) before expiring subscribers
    user: APINullable[:class:`~pincer.objects.user.user.User`]
        User for this integration
    synced_at: APINullable[:class:`~pincer.utils.timestamp.Timestamp`]
        When this integration was last synced
    subscriber_count: APINullable[:class:`int`]
        How many subscribers this integration has
    revoked: APINullable[:class:`bool`]
        Has this integration been revoked
    application: APINullable[:class:`~pincer.objects.user.integration.IntegrationApplication`]
        The bot/OAuth2 application for discord integrations
    """
    # noqa: E501

    id: Snowflake
    name: str
    type: str
    enabled: bool
    account: IntegrationAccount

    syncing: APINullable[bool] = MISSING
    role_id: APINullable[Snowflake] = MISSING
    enable_emoticons: APINullable[bool] = MISSING
    expire_behavior: APINullable[IntegrationExpireBehavior] = MISSING
    expire_grace_period: APINullable[int] = MISSING
    user: APINullable[User] = MISSING
    synced_at: APINullable[Timestamp] = MISSING
    subscriber_count: APINullable[int] = MISSING
    revoked: APINullable[bool] = MISSING
    application: APINullable[IntegrationApplication] = MISSING
