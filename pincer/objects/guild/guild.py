# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import overload, TYPE_CHECKING

from .channel import Channel
from .member import GuildMember
from ...exceptions import UnavailableGuildError
from ...utils.api_object import APIObject
from ...utils.conversion import construct_client_dict
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Union

    from .features import GuildFeature
    from .role import Role
    from .stage import StageInstance
    from .welcome_screen import WelcomeScreen
    from ..events.presence import PresenceUpdateEvent
    from ..message.emoji import Emoji
    from ..message.sticker import Sticker
    from ..user.voice_state import VoiceState
    from ...client import Client
    from ...utils.timestamp import Timestamp
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


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
    """

    # noqa: E501
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
    SUPPRESS_JOIN_NOTIFICATION_REPLIES:
        Hide member join sticker reply buttons
    """

    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3


@dataclass
class Guild(APIObject):
    """Represents a Discord guild/server in which your client resides.

    Attributes
    ----------
    afk_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of afk channel
    afk_timeout: :class:`int`
        Afk timeout in seconds
    application_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        Application id of the guild creator if it is bot-created
    banner: Optional[:class:`str`]
        Banner hash
    default_message_notifications: :class:`~pincer.objects.guild.guild.DefaultMessageNotificationLevel`
        Default message notifications level
    description: Optional[:class:`str`]
        The description of a Community guild
    discovery_splash: Optional[:class:`str`]
        Discovery splash hash;
        only present for guilds with the "DISCOVERABLE" feature
    emojis: List[:class:`~pincer.objects.message.emoji.Emoji`]
        Custom guild emojis
    explicit_content_filter: :class:`~pincer.objects.guild.guild.ExplicitContentFilterLevel`
        Explicit content filter level
    features: List[:class:`~pincer.objects.guild.features.GuildFeature`]
        Enabled guild features
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Guild id
    icon: Optional[:class:`str`]
        Icon hash
    mfa_level: :class:`~pincer.objects.guild.guild.MFALevel`
        Required MFA level for the guild
    name: :class:`str`
        Guild name (2-100 characters, excluding trailing and leading
        whitespace)
    nsfw_level: :class:`~pincer.objects.guild.guild.NSFWLevel`
        Guild NSFW level
    owner_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of owner
    preferred_locale: :class:`str`
        The preferred locale of a Community guild;
        used in server discovery and notices from Discord;
        defaults to "en-US"
    premium_tier: :class:`~pincer.objects.guild.guild.PremiumTier`
        Premium tier (Server Boost level)
    public_updates_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the channel where admins
        and moderators of Community guilds receive notices from Discord
    roles: List[:class:`~pincer.objects.guild.role.Role`]
        Roles in the guild
    rules_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the channel where Community guilds can display rules
        and/or guidelines
    splash: Optional[:class:`str`]
        Splash hash
    system_channel_flags: :class:`~pincer.objects.guild.guild.SystemChannelFlags`
        System channel flags
    system_channel_id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the channel where guild notices
        such as welcome messages and boost events are posted
    vanity_url_code: Optional[:class:`str`]
        The vanity url code for the guild
    verification_level: :class:`~pincer.objects.guild.guild.VerificationLevel`
        Verification level required for the guild
    approximate_member_count: APINullable[:class:`int`]
        Approximate number of members in this guild, returned from the
        `GET /guilds/<id>` endpoint when with_counts is true
    approximate_presence_count: APINullable[:class:`int`]
        Approximate number of non-offline members in this guild,
        returned from the `GET /guilds/<id>`
        endpoint when with_counts is true
    channels: APINullable[List[:class:`~pincer.objects.guild.channel.Channel`]]
        Channels in the guild
    icon_hash: APINullable[Optional[:class:`str`]]
        Icon hash, returned when in the template object
    joined_at: APINullable[:class:`~pincer.utils.timestamp.Timestamp`]
        When this guild was joined at
    large: APINullable[:class:`bool`]
        True if this is considered a large guild
    max_members: APINullable[:class:`int`]
        The maximum number of members for the guild
    max_presences: APINullable[Optional[:class:`int`]]
        The maximum number of presences for the guild
        (null is always returned, apart from the largest of guilds)
    max_video_channel_users: APINullable[:class:`int`]
        The maximum amount of users in a video channel
    members: APINullable[List[:class:`~pincer.objects.guild.member.GuildMember`]]
        Users in the guild
    member_count: APINullable[:class:`bool`]
        Total number of members in this guild
    nsfw: APINullable[:class:`bool`]
        Boolean if the server is NSFW
    owner: APINullable[:class:`bool`]
        True if the user is the owner of the guild
    permissions: APINullable[:class:`str`]
        Total permissions for the user in the guild
        (excludes overwrites)
    premium_subscription_count: APINullable[:class:`int`]
        The number of boosts this guild currently has
    presences: APINullable[List[:class:`~pincer.objects.events.presence.PresenceUpdateEvent`]]
        Presences of the members in the guild,
        will only include non-offline members if the size is greater
        than large threshold
    stage_instances: APINullable[List[:class:`~pincer.objects.guild.stage.StageInstance`]]
        Stage instances in the guild
    stickers: Optional[List[:class:`~pincer.objects.message.sticker.Sticker`]]
        Custom guild stickers
    region: APINullable[Optional[:class:`str`]]
        Voice region id for the guild (deprecated)
    threads: APINullable[List[:class:`~pincer.objects.guild.channel.Channel`]]
        All active threads in the guild that current user
        has permission to view
    unavailable: APINullable[:class:`bool`]
        True if this guild is unavailable due to an outage
    voice_states: APINullable[List[:class:`~pincer.objects.user.voice_state.VoiceState`]]
        States of members currently in voice channels;
        lacks the guild_id key
    widget_enabled: APINullable[:class:`bool`]
        True if the server widget is enabled
    widget_channel_id: APINullable[Optional[:class:`~pincer.utils.snowflake.Snowflake`]]
        The channel id that the widget will generate an invite to,
        or null if set to no invite
    welcome_screen: APINullable[:class:`~pincer.objects.guild.welcome_screen.WelcomeScreen`]
        The welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    """

    # noqa: E501
    afk_timeout: int
    default_message_notifications: DefaultMessageNotificationLevel
    emojis: List[Emoji]
    explicit_content_filter: ExplicitContentFilterLevel
    features: List[GuildFeature]
    id: Snowflake
    mfa_level: MFALevel
    name: str
    nsfw_level: GuildNSFWLevel
    owner_id: Snowflake
    preferred_locale: str
    premium_tier: PremiumTier
    roles: List[Role]
    system_channel_flags: SystemChannelFlags
    verification_level: VerificationLevel

    guild_scheduled_events: APINullable[List] = MISSING
    lazy: APINullable[bool] = MISSING
    premium_progress_bar_enabled: APINullable[bool] = MISSING
    guild_hashes: APINullable[Dict] = MISSING
    afk_channel_id: APINullable[Snowflake] = MISSING
    application_id: APINullable[Snowflake] = MISSING
    embedded_activities: APINullable[List] = MISSING
    banner: APINullable[str] = MISSING
    description: APINullable[str] = MISSING
    discovery_splash: APINullable[str] = MISSING
    icon: APINullable[str] = MISSING
    public_updates_channel_id: APINullable[Snowflake] = MISSING
    rules_channel_id: APINullable[Snowflake] = MISSING
    splash: APINullable[str] = MISSING
    system_channel_id: APINullable[Snowflake] = MISSING
    vanity_url_code: APINullable[str] = MISSING

    application_command_counts: APINullable[Dict] = MISSING
    application_command_count: APINullable[int] = MISSING
    approximate_member_count: APINullable[int] = MISSING
    approximate_presence_count: APINullable[int] = MISSING
    channels: APINullable[List[Channel]] = field(default_factory=list)
    # TODO: Add type when type is known
    hub_type: APINullable[Any] = MISSING
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
    voice_states: APINullable[List[VoiceState]] = MISSING
    widget_enabled: APINullable[bool] = MISSING
    widget_channel_id: APINullable[Optional[Snowflake]] = MISSING
    welcome_screen: APINullable[WelcomeScreen] = MISSING

    @classmethod
    async def from_id(cls, client: Client, _id: Union[int, Snowflake]) -> Guild:
        """
        Parameters
        ----------
        client : `~pincer.Client`
            Client object to use the http gateway from.
        _id : :class: `pincer.utils.snowflake.Snowflake`
            Guild ID.

        Returns
        -------
        :class: `~pincer.objects.guild.guild.Guild`
            The new guild object.
        """
        data = await client.http.get(f"/guilds/{_id}")
        channel_data = await client.http.get(f"/guilds/{_id}/channels")

        data["channels"]: List[Channel] = [
            Channel.from_dict({**i, "_client": client, "_http": client.http})
            for i in (channel_data or [])
        ]

        return Guild.from_dict(construct_client_dict(client, data))

    async def get_member(self, _id: int) -> GuildMember:
        """|coro|

        Fetches a GuildMember from its identifier

        Parameters
        ----------
        _id:
            The id of the guild member which should be fetched from the Discord
            gateway.

        Returns
        -------
        :class:`~pincer.objects.guild.member.GuildMember`
            A GuildMember object.
        """
        return await GuildMember.from_id(self._client, self.id, _id)

    @overload
    async def modify_member(
        self,
        *,
        _id: int,
        nick: Optional[str] = None,
        roles: Optional[List[Snowflake]] = None,
        mute: Optional[bool] = None,
        deaf: Optional[bool] = None,
        channel_id: Optional[Snowflake] = None,
    ) -> GuildMember:
        """|coro|

        Modifies a member in the guild from its identifier and based on the
        keyword arguments provided.

        Parameters
        ----------
        _id : int
            Id of the member to modify
        nick : Optional[:class:`str`]
            New nickname for the member |default| :data:`None`
        roles : Optional[List[:class:`~pincer.utils.snowflake.Snowflake]]
            New roles for the member |default| :data:`None`
        mute : Optional[:class:`bool`]
            Whether the member is muted |default| :data:`None`
        deaf : Optional[:class:`bool`]
            Whether the member is deafened |default| :data:`None`
        channel_id : Optional[:class:`~pincer.utils.snowflake.Snowflake]
            Voice channel id to move to |default| :data:`None`

        Returns
        -------
        :class:`~pincer.objects.guild.member.GuildMember`
            The new member object.
        """
        ...

    async def modify_member(self, _id: int, **kwargs) -> GuildMember:
        data = await self._http.patch(
            f"guilds/{self.id}/members/{_id}", data=kwargs
        )
        return GuildMember.from_dict(construct_client_dict(self._client, data))

    async def kick(self, member_id: int):
        """|coro|
        Kicks a guild member.

        Parameters
        ----------
        member_id : :class: int
            ID of the guild member to kick.
        """
        await self._http.delete(f"/guilds/{self.id}/members/{member_id}")

    async def ban(self, member_id: int, **kwargs):
        """|coro|
        Bans a guild member.

        Parameters
        ----------
        member_id : :class: int
            ID of the guild member to ban.
        \\*\\* kwargs
            Additional keyword arguments to kick the guild member with.
        """
        await self._http.put(f"/guilds/{self.id}/bans/{member_id}", data=kwargs)

    @classmethod
    def from_dict(cls, data) -> Guild:
        """
        Parameters
        ----------
        data : :class: Dict
            Guild data received from the discord API.

        Returns
        -------
        :class: `~pincer.objects.guild.guild.Guild`
            The new guild object.

        Raises
        :class: `~pincer.exceptions.UnavailableGuildError`
            The guild is unavailable due to a discord outage.
        """
        if data.get("unavailable", False):
            raise UnavailableGuildError(
                f"Guild \"{data['id']}\" is unavailable due to a discord"
                " outage."
            )

        return super().from_dict(data)


@dataclass
class UnavailableGuild(APIObject):
    id: Snowflake
    unavailable: bool = True
