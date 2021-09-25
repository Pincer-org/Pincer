# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto, IntEnum
from typing import Optional, List, overload, TYPE_CHECKING

from pincer.objects.events.presence import PresenceUpdateEvent
from ..exceptions import UnavailableGuildError
from .channel import Channel
from .emoji import Emoji
from .guild_member import GuildMember
from .role import Role
from .stage import StageInstance
from .sticker import Sticker
from .voice_state import VoiceState
from .welcome_screen import WelcomeScreen
from ..utils import APIObject, APINullable, MISSING, Snowflake, Timestamp

if TYPE_CHECKING:
    from pincer import Client
    from pincer.core.http import HTTPClient


class PremiumTier(IntEnum):
    """
    :param NONE:
        guild has not unlocked any Server Boost perks

    :param TIER_1:
        guild has unlocked Server Boost level 1 perks

    :param TIER_2:
        guild has unlocked Server Boost level 2 perks

    :param TIER_3:
        guild has unlocked Server Boost level 3 perks
    """
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


class GuildNSFWLevel(IntEnum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class ExplicitContentFilterLevel(IntEnum):
    """
    :param DISABLED:
        media content will not be scanned

    :param MEMBERS_WITHOUT_ROLES:
        media content sent by members without roles will be scanned

    :param ALL_MEMBERS:
        media content sent by all members will be scanned
    """
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(IntEnum):
    """
    :param NONE:
        guild has no MFA/2FA requirement for moderation actions

    :param ELEVATED:
        guild has a 2FA requirement for moderation actions
    """
    NONE = 0
    ELEVATED = 1


class VerificationLevel(IntEnum):
    """
    :param NONE:
        unrestricted

    :param LOW:
        must have verified email on account

    :param MEDIUM:
        must be registered on Discord for longer than 5 minutes

    :param HIGH:
        must be a member of the server for longer than 10 minutes

    :param VERY_HIGH:
        must have a verified phone number
    """
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class DefaultMessageNotificationLevel(IntEnum):
    """
    :param ALL_MESSAGES:
        members will receive notifications for all messages by default

    :param ONLY_MENTIONS:
        members will receive notifications only
        for messages that @mention them by default
    """
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class SystemChannelFlags(IntEnum):
    """
    :param SUPPRESS_JOIN_NOTIFICATIONS:
        Suppress member join notifications

    :param SUPPRESS_PREMIUM_SUBSCRIPTIONS:
        Suppress server boost notifications

    :param SUPPRESS_GUILD_REMINDER_NOTIFICATIONS:
        Suppress server setup tips
    """
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2


class GuildFeature(Enum):
    """
    :param ANIMATED_ICON:
        guild has access to set an animated guild icon

    :param BANNER:
        guild has access to set a guild banner image

    :param COMMERCE:
        guild has access to use commerce features (i.e. create store channels)

    :param COMMUNITY:
        guild can enable welcome screen, Membership Screening, stage channels
        and discovery, and receives community updates

    :param DISCOVERABLE:
        guild is able to be discovered in the directory

    :param FEATURABLE:
        guild is able to be featured in the directory

    :param INVITE_SPLASH:
        guild has access to set an invite splash background

    :param MEMBER_VERIFICATION_GATE_ENABLED:
        guild has enabled Membership Screening

    :param NEWS:
        guild has access to create news channels

    :param PARTNERED:
        guild is partnered

    :param PREVIEW_ENABLED:
        guild can be previewed before joining via Membership Screening
        or the directory

    :param VANITY_URL:
        guild has access to set a vanity URL

    :param VERIFIED:
        guild is verified

    :param VIP_REGIONS:
        guild has access to set 384kbps bitrate in voice
        (previously VIP voice servers)

    :param WELCOME_SCREEN_ENABLED:
        guild has enabled the welcome screen

    :param TICKETED_EVENTS_ENABLED:
        guild has enabled ticketed events

    :param MONETIZATION_ENABLED:
        guild has enabled monetization

    :param MORE_STICKERS:
        guild has increased custom sticker slots

    :param THREE_DAY_THREAD_ARCHIVE:
        guild has access to the three day archive time for threads

    :param SEVEN_DAY_THREAD_ARCHIVE:
        guild has access to the seven day archive time for threads

    :param PRIVATE_THREADS:
        guild has access to create private threads
    """
    ANIMATED_ICON = auto()
    BANNER = auto()
    COMMERCE = auto()
    COMMUNITY = auto()
    DISCOVERABLE = auto()
    FEATURABLE = auto()
    INVITE_SPLASH = auto()
    MEMBER_VERIFICATION_GATE_ENABLED = auto()
    NEWS = auto()
    PARTNERED = auto()
    PREVIEW_ENABLED = auto()
    VANITY_URL = auto()
    VERIFIED = auto()
    VIP_REGIONS = auto()
    WELCOME_SCREEN_ENABLED = auto()
    TICKETED_EVENTS_ENABLED = auto()
    MONETIZATION_ENABLED = auto()
    MORE_STICKERS = auto()
    THREE_DAY_THREAD_ARCHIVE = auto()
    SEVEN_DAY_THREAD_ARCHIVE = auto()
    PRIVATE_THREADS = auto()


@dataclass
class Guild(APIObject):
    """
    Represents a Discord guild/server in which your client resides.

    :param _client:
        reference to the Client

    :param _http:
        reference to the HTTPClient

    :param afk_channel_id:
        id of afk channel

    :param afk_timeout:
        afk timeout in seconds

    :param application_id:
        application id of the guild creator if it is bot-created

    :param banner:
        banner hash

    :param default_message_notifications:
        default message notifications level

    :param description:
        the description of a Community guild

    :param discovery_splash:
        discovery splash hash;
        only present for guilds with the "DISCOVERABLE" feature

    :param emojis:
        custom guild emojis

    :param explicit_content_filter:
        explicit content filter level

    :param features:
        enabled guild features

    :param id:
        guild id

    :param icon:
        icon hash

    :param mfa_level:
        required MFA level for the guild

    :param name:
        guild name (2-100 characters, excluding trailing and leading
        whitespace)

    :param nsfw_level:
        guild NSFW level

    :param owner_id:
        id of owner

    :param preferred_locale:
        the preferred locale of a Community guild;
        used in server discovery and notices from Discord;
        defaults to "en-US"

    :param premium_tier:
        premium tier (Server Boost level)

    :param public_updates_channel_id:
        the id of the channel where admins
        and moderators of Community guilds receive notices from Discord

    :param roles:
        roles in the guild

    :param rules_channel_id:
        the id of the channel where Community guilds can display rules
        and/or guidelines

    :param splash:
        splash hash

    :param system_channel_flags:
        system channel flags

    :param system_channel_id:
        the id of the channel where guild notices
        such as welcome messages and boost events are posted

    :param vanity_url_code:
        the vanity url code for the guild

    :param verification_level:
        verification level required for the guild

    :param approximate_member_count:
        approximate number of members in this guild, returned from the
        `GET /guilds/<id>` endpoint when with_counts is true

    :param approximate_presence_count:
        approximate number of non-offline members in this guild,
        returned from the `GET /guilds/<id>`
        endpoint when with_counts is true

    :param channels:
        channels in the guild

    :param icon_hash:
        icon hash, returned when in the template object

    :param joined_at:
        when this guild was joined at

    :param large:
        true if this is considered a large guild

    :param max_members:
        the maximum number of members for the guild

    :param max_presences:
        the maximum number of presences for the guild
        (null is always returned, apart from the largest of guilds)

    :param max_video_channel_users:
        the maximum amount of users in a video channel

    :param members:
        users in the guild

    :param member_count:
        total number of members in this guild

    :param nsfw:
        boolean if the server is NSFW

    :param owner:
        true if the user is the owner of the guild

    :param permissions:
        total permissions for the user in the guild
        (excludes overwrites)

    :param premium_subscription_count:
        the number of boosts this guild currently has

    :param presences:
        presences of the members in the guild,
        will only include non-offline members if the size is greater
        than large threshold

    :param stage_instances:
        Stage instances in the guild

    :param stickers:
        custom guild stickers

    :param region:
        voice region id for the guild (deprecated)

    :param threads:
        all active threads in the guild that current user
        has permission to view

    :param unavailable:
        true if this guild is unavailable due to an outage

    :param voice_states:
        states of members currently in voice channels;
        lacks the guild_id key

    :param widget_enabled:
        true if the server widget is enabled

    :param widget_channel_id:
        the channel id that the widget will generate an invite to,
        or null if set to no invite

    :param welcome_screen:
        the welcome screen of a Community guild, shown to new members,
        returned in an Invite's guild object
    """

    _client: Client
    _http: HTTPClient

    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    application_id: Optional[Snowflake]
    banner: Optional[str]
    default_message_notifications: DefaultMessageNotificationLevel
    description: Optional[str]
    discovery_splash: Optional[str]
    emojis: List[Emoji]
    explicit_content_filter: ExplicitContentFilterLevel
    features: List[GuildFeature]
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
    voice_states: APINullable[List[VoiceState]] = MISSING
    widget_enabled: APINullable[bool] = MISSING
    widget_channel_id: APINullable[Optional[Snowflake]] = MISSING
    welcome_screen: APINullable[WelcomeScreen] = MISSING

    @classmethod
    async def from_id(cls, client: Client, _id: int) -> Guild:
        data = await client.http.get(f"/guilds/{_id}")
        channel_data = await client.http.get(f"/guilds/{_id}/channels")

        channels: List[Channel] = [
            Channel.from_dict(i | {"_client": client, "_http": client.http})
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

        :param _id:
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

    async def modify_member(self, _id: int, **kwargs) -> GuildMember:
        data = await self._http.patch(f"guilds/{self.id}/members/{_id}", kwargs)
        return GuildMember.from_dict(
            data | {"_client": self._client, "_http": self._http}
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
