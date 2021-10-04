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
    from ...utils import APINullable, Snowflake, Timestamp


class IntegrationExpireBehavior(IntEnum):
    """Represents a Discord Integration expire behavior"""
    REMOVE_ROLE = 0
    KICK = 1


@dataclass
class IntegrationAccount(APIObject):
    """
    Represents a Discord Integration Account object

    :param id:
        id of the account

    :param name:
        name of the account
    """
    id: str
    name: str


@dataclass
class IntegrationApplication(APIObject):
    """
    Represents a Discord Integration Application object

    :param id:
        the id of the app

    :param name:
        the name of the app

    :param icon:
        the icon hash of the app

    :param description:
        the description of the app

    :param summary:
        the summary of the app

    :param bot:
        the bot associated with this application
    """
    id: Snowflake
    name: str
    icon: Optional[str]
    description: str
    summary: str
    bot: APINullable[User] = MISSING


@dataclass
class Integration(APIObject):
    """
    Represents a Discord Integration object

    :param id:
        integration id

    :param name:
        integration name

    :param type:
        integration type (twitch, youtube, or discord)$

    :param enabled:
        is this integration enabled

    :param syncing:
        is this integration syncing

    :param role_id:
        id that this integration uses for subscribers

    :param enable_emoticons:
        whether emoticons should be synced for this integration
        (twitch only currently)

    :param expire_behavior:
        the behavior of expiring subscribers

    :param expire_grace_period:
        the grace period (in days) before expiring subscribers

    :param user:
        user for this integration

    :param account:
        integration account information

    :param synced_at:
        when this integration was last synced

    :param subscriber_count:
        how many subscribers this integration has

    :param revoked:
        has this integration been revoked

    :param application:
        The bot/OAuth2 application for discord integrations
    """

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
