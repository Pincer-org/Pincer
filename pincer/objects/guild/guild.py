# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from typing import overload, TYPE_CHECKING
from enum import IntEnum
from dataclasses import dataclass, field

from ...utils.types import MISSING
from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Dict, List, Optional

    from .role import Role
    from .channel import Channel
    from ...client import Client
    from ..user import voice_state
    from .member import GuildMember
    from .stage import StageInstance
    from ..message.emoji import Emoji
    from .features import GuildFeatures
    from ..message.sticker import Sticker
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp
    from .welcome_screen import WelcomeScreen
    from ...exceptions import UnavailableGuildError
    from ..events.presence import PresenceUpdateEvent


class PremiumTier(IntEnum):
    """Represents the boost tier of a guild.

    Attributes
    ----------
    NONE:
        Guild has not unlocked any Server Boost perks.
    TIER_1:
        Guild has unlocked Server Boost level 1 perks.
    TIER_2:
        Guild has unlocked Server Boost level 2 perks.
    TIER_3:
        Guild has unlocked Server Boost level 3 perks.
    """
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class GuildNSFWLevel(IntEnum):
    """Represents the NSFW level of a guild.

    Attributes
    ----------
    DEFAULT:
        Default NSFW level.
    EXPLICIT:
        Explicit NSFW level.
    SAFE:
        SAFE NSFW level.
    AGE_RESTRICTED:
        Age restricted NSFW level.
    """
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class ExplicitContentFilterLevel(IntEnum):
    """Represents the filter content level of a guild.

    Attributes
    ----------
    DISABLED:
        Media content will not be scanned.
    MEMBERS_WITHOUT_ROLES:
        Media content sent by members without roles will be scanned.
    ALL_MEMBERS:
        Media content sent by all members will be scanned.
    """
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(IntEnum):
    """Represents the multi factor authentication level of a guild.

    Attributes
    ----------
    NONE:
        Guild has no MFA/2FA requirement for moderation actions.
    ELEVATED:
        Guild has a 2FA requirement for moderation actions
    """
    NONE = 0
    ELEVATED = 1


class VerificationLevel(IntEnum):
    """Represents the verification level of a guild.

    Attributes
    ----------
    NONE:
        Unrestricted.
    LOW:
        Must have verified email on account.
    MEDIUM:
        Must be registered on Discord for longer than 5 minutes.
    HIGH:
        Must be a member of the server for longer than 10 minutes.
    VERY_HIGH:
        Must have a verified phone number.
    """
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class DefaultMessageNotificationLevel(IntEnum):
    """Represents the default message notification level of a guild.

    Attributes
    ----------
    ALL_MESSAGES:
        Members will receive notifications for all messages by default.
    ONLY_MENTIONS:
        Members will receive notifications only for messages that @mention them by default.
    """  # noqa: E501
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class SystemChannelFlags(IntEnum):
    """Represents the system channel flags of a guild.

    Attributes
    ----------
    SUPPRESS_JOIN_NOTIFICATIONS:
        Suppress member join notifications.
    SUPPRESS_PREMIUM_SUBSCRIPTIONS:
        Suppress server boost notifications.
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS:
        Suppress server setup tips.
    """
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2


@dataclass
class Guild(APIObject):
    """Represents a Discord guild/server in which your client resides.

    Attributes
    ----------
    afk_channel_id:
        id of afk channel
    afk_timeout:
        afk timeout in seconds
    application_id:
        application id of the guild creator if it is bot-created
    banner:
        banner hash
    default_message_notifications:
        default message notifications level
    description:
        the description of a Community guild
    discovery_splash:
        discovery splash hash;
        only present for guilds with the "DISCOVERABLE" feature
    emojis:
        custom guild emojis
    explicit_content_filter:
        explicit content filter level
    features:
        enabled guild features
    id:
        guild id
    icon:
        icon hash
    mfa_level:
        required MFA level for the guild
    name:
        guild name (2-100 characters, excluding trailing and leading
        whitespace)
    nsfw_level:
        guild NSFW level
    owner_id:
        id of owner
    preferred_locale:
        the preferred locale of a Community guild;
        used in server discovery and notices from Discord;
        defaults to "en-US"
    premium_tier:
        premium tier (Server Boost level)
    public_updates_channel_id:
        the id of the channel where admins
        and moderators of Community guilds receive notices from Discord
    roles:
        roles in the guild
    rules_channel_id:
        the id of the channel where Community guilds can display rules
        and/or guidelines
    splash:
        splash hash
    system_channel_flags:
        system channel flags
    system_channel_id:
        the id of the channel where guild notices
        such as welcome messages and boost events are posted
    vanity_url_code:
        the vanity url code for the guild
    verification_level:
        verification level required for the guild
    approximate_member_count:
        approximate number of members in this guild, returned from the
        `GET /guilds/<id>` endpoint when with_counts is true
    approximate_presence_count:
        approximate number of non-offline members in this guild,
        returned from the `GET /guilds/<id>`
        endpoint when with_counts is true
    channels:
        channels in the guild
    icon_hash:
        icon hash, returned when in the template object
    joined_at:
        when this guild was joined at
    large:
        true if this is considered a large guild
    max_members:
        the maximum number of members for the guild
    max_presences:
        the maximum number of presences for the guild
        (null is always returned, apart from the largest of guilds)
    max_video_channel_users:
        the maximum amount of users in a video channel
    members:
        users in the guild
    member_count:
        total number of members in this guild
    nsfw:
        boolean if the server is NSFW
    owner:
        true if the user is the owner of the guild
    permissions:
        total permissions for the user in the guild
        (excludes overwrites)
    premium_subscription_count:
        the number of boosts this guild currently has
    presences:
        presences of the members in the guild,
        will only include non-offline members if the size is greater
        than large threshold
    stage_instances:
        Stage instances in the guild
    stickers:
        custom guild stickers
    region:
        voice region id for the guild (deprecated)
    threads:
        all active threads in the guild that current user
        has permission to view
    unavailable:
        true if this guild is unavailable due to an outage
    voice_states:
        states of members currently in voice channels;
        lacks the guild_id key
    widget_enabled:
        true if the server widget is enabled
    widget_channel_id:
        the channel id that the widget will generate an invite to,
        or null if set to no invite
    welcome_screen:
        the welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    """
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    application_id: Optional[Snowflake]
    embedded_activities: Optional[List]
    banner: Optional[str]
    default_message_notifications: DefaultMessageNotificationLevel
    description: Optional[str]
    discovery_splash: Optional[str]
    emojis: List[Emoji]
    explicit_content_filter: ExplicitContentFilterLevel
    features: List[GuildFeatures]
    id: Snowflake
    icon: Optional[str]
    mfa_level: MFALevel
    name: str
    nsfw_level: GuildNSFWLevel
    owner_id: Snowflake
    preferred_locale: str
    premium_tier: PremiumTier
    public_updates_channel_id: Optional[Snowflake]
    roles: List[Role]
    rules_channel_id: Optional[Snowflake]
    splash: Optional[str]
    system_channel_flags: SystemChannelFlags
    system_channel_id: Optional[Snowflake]
    vanity_url_code: Optional[str]
    verification_level: VerificationLevel
    guild_scheduled_events: Optional[List]
    lazy: Optional[bool]
    premium_progress_bar_enabled: Optional[bool]
    guild_hashes: Optional[Dict]

    application_command_counts: APINullable[Dict] = MISSING
    application_command_count: APINullable[int] = MISSING
    approximate_member_count: APINullable[int] = MISSING
    approximate_presence_count: APINullable[int] = MISSING
    channels: APINullable[List[Channel]] = field(default_factory=list)
    # TODO: Add type when type is known
    hub_type: APINullable[...] = MISSING
    icon_hash: APINullable[Optional[str]] = MISSING
    joined_at: APINullable[Timestamp] = MISSING
    large: APINullable[bool] = MISSING
    max_members: APINullable[int] = MISSING
    max_presences: APINullable[Optional[int]] = MISSING
    max_video_channel_users: APINullable[int] = MISSING
    members: APINullable[List[GuildMember]] = MISSING
    member_count: APINullable[bool] = MISSING
    nsfw: APINullable[bool] = MISSING
    # Note: This is missing from discord's docs but in the api
    owner: APINullable[bool] = MISSING
    permissions: APINullable[str] = MISSING
    premium_subscription_count: APINullable[int] = MISSING
    presences: APINullable[List[PresenceUpdateEvent]] = MISSING
    stage_instances: APINullable[List[StageInstance]] = MISSING
    stickers: APINullable[List[Sticker]] = MISSING
    region: APINullable[Optional[str]] = MISSING
    threads: APINullable[List[Channel]] = MISSING
    # Guilds are considered available unless otherwise specified
    unavailable: APINullable[bool] = False
    voice_states: APINullable[List[voice_state.VoiceState]] = MISSING
    widget_enabled: APINullable[bool] = MISSING
    widget_channel_id: APINullable[Optional[Snowflake]] = MISSING
    welcome_screen: APINullable[WelcomeScreen] = MISSING

    @classmethod
    async def from_id(cls, client: Client, _id: int) -> Guild:
        data = await client.http.get(f"/guilds/{_id}")
        channel_data = await client.http.get(f"/guilds/{_id}/channels")

        channels: List[Channel] = [
            Channel.from_dict({**i, "_client": client, "_http": client.http})
            for i in (channel_data or [])
        ]

        data.update(
            {
                "_client": client,
                "_http": client.http,
                "channels": channels
            }
        )

        # Once below is fixed. Change this to Guild.from_dict
        return Guild(**data)

    async def get_member(self, _id: int):
        """
        Fetches a GuildMember from its identifier

        _id:
            The id of the guild member which should be fetched from the Discord
            gateway.

        :returns:
            A GuildMember objects.

        """
        return await GuildMember.from_id(self._client, self.id, _id)

    @overload
    async def modify_member(
            self, *,
            _id: int,
            nick: Optional[str] = None,
            roles: Optional[List[Snowflake]] = None,
            mute: Optional[bool] = None,
            deaf: Optional[bool] = None,
            channel_id: Optional[Snowflake] = None
    ) -> GuildMember:
        """
        Modifies a member in the guild from its identifier and based on the
        keyword arguments provided.

        :returns:
            The GuildMember that has been modified.
        """
        ...

    async def modify_member(self, _id: int, **kwargs) -> GuildMember:
        data = await self._http.patch(f"guilds/{self.id}/members/{_id}", kwargs)
        return GuildMember.from_dict(
            {**data, "_client": self._client, "_http": self._http}
        )

    @classmethod
    def from_dict(cls, data) -> Guild:
        """
        Instantiate a new guild from a dictionary.

        Also handles it if the guild isn't available.

        :raises UnavailableGuildError:
            Exception gets raised when guild is unavailable.
        """
        if data.get("unavailable", False):
            raise UnavailableGuildError(
                f"Guild \"{data['id']}\" is unavailable due"
                " to a discord outage."
            )

        return super().from_dict(data)
