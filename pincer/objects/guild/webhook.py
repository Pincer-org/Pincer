# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Optional

    from ..user.user import User
    from ..guild.guild import Guild
    from ..guild.channel import Channel
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


class WebhookType(IntEnum):
    """Represents the type of a webhook.

    Attributes
    ----------
    INCOMING:
        Incoming Webhooks can post messages to channels with a
        generated token.
    CHANNEL_FOLLOWER:
        Channel Follower Webhooks are internal webhooks used with
        Channel Following to post new messages into channels.
    APPLICATION:
        Application webhooks are webhooks used with Interactions
    """
    INCOMING = 1
    CHANNEL_FOLLOWER = 2
    APPLICATION = 3


@dataclass
class Webhook(APIObject):
    """Represents a Discord channel webhook.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the webhook
    type: :class:`~pincer.objects.guild.webhook.WebhookType`
        The type of the webhook
    channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The channel id this webhook is for, if any
    name: Optional[:class:`str`]
        The default name of the webhook
    avatar: Optional[:class:`str`]
        The default user avatar hash of the webhook
    application_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The bot/OAuth2 application that created this webhook
    user: APINullable[:class:`~pincer.objects.user.user.User`]
        The user this webhook was created by
        (not returned when getting a webhook with its token)
    token: APINullable[:class:`str`]
        The secure token of the webhook
        (returned for Incoming Webhooks)
    source_guild: APINullable[:class:`~pincer.objects.guild.guild.Guild`]
        The guild of the channel that this webhook is following
        (returned for Channel Follower Webhooks)
    source_channel: APINullable[:class:`~pincer.objects.guild.channel.Channel`]
        The channel that this webhook is following
        (returned for Channel Follower Webhooks)
    url: APINullable[:class:`str`]
        The url used for executing the webhook
        (returned by the webhooks OAuth2 flow)
    guild_id: APINullable[Optional[:class:`~pincer.objects.guild.guild.Guild`]]
        The guild id this webhook is for, if any
    """
    id: Snowflake
    type: WebhookType

    channel_id: Optional[Snowflake] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    application_id: Optional[Snowflake] = None

    user: APINullable[User] = MISSING
    token: APINullable[str] = MISSING
    source_guild: APINullable[Guild] = MISSING
    source_channel: APINullable[Channel] = MISSING
    url: APINullable[str] = MISSING

    guild_id: APINullable[Optional[Snowflake]] = MISSING
