# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import overload, TYPE_CHECKING, Union

from .channel import Channel
from .member import GuildMember
from ...exceptions import UnavailableGuildError
from ...utils.api_object import APIObject
from ...utils.conversion import construct_client_dict
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Tuple
    from .channel import PublicThread, PrivateThread
    from .features import GuildFeature
    from .overwrite import Overwrite
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
        client : :class:`~pincer.Client`
            Client object to use the http gateway from.
        _id : :class:`pincer.utils.snowflake.Snowflake`
            Guild ID.

        Returns
        -------
        :class:`~pincer.objects.guild.guild.Guild`
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
        _id: int
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
            self, *,
            _id: int,
            nick: Optional[str] = None,
            roles: Optional[List[Snowflake]] = None,
            mute: Optional[bool] = None,
            deaf: Optional[bool] = None,
            channel_id: Optional[Snowflake] = None
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
            f"guilds/{self.id}/members/{_id}",
            data=kwargs
        )
        return GuildMember.from_dict(construct_client_dict(self._client, data))

    @overload
    async def create_channel(self, name: str,
                             type: Optional[int] = None,
                             topic: Optional[str] = None,
                             bitrate: Optional[int] = None,
                             user_limit: Optional[int] = None,
                             rate_limit_per_user: Optional[int] = None,
                             position: Optional[int] = None,
                             permission_overwrites: Optional[
                                 List[Overwrite]] = None,
                             parent_id: Optional[Snowflake] = None,
                             nsfw: Optional[bool] = None) -> Channel:
        """|coro|
        Create a new channel object for the guild.

        Parameters
        ----------
        name : str
            channel name (1-100 characters)
        type : Optional[int]
            the type of channel
        topic : Optional[str]
            channel topic (0-1024 characters)
        bitrate : `Optional[int]
            the bitrate (in bits) of the voice channel (voice only)
        user_limit : `Optional[int]
            the user limit of the voice channel (voice only)
        rate_limit_per_user : `Optional[int]
            amount of seconds a user has to wait before sending another message (0-21600)
            bots, as well as users with the permission manage_messages or manage_channel, are unaffected
        position : Optional[int]
            sorting position of the channel
        permission_overwrites : Optional[List[:class:`~pincer.objects.guild.overwrite.Overwrite`]]
            the channel's permission overwrites
        parent_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]
            id of the parent category for a channel
        nsfw : `Optional[bool]
            whether the channel is nsfw

        """
        ...

    async def create_channel(self, **kwargs):
        data = await self._http.post(f"guilds/{self.id}/channels", data=kwargs)
        return Channel.from_dict(construct_client_dict(self._client, data=data))

    async def modify_channel_positions(
            self, *channel: Dict[str, Optional[Union[int, bool, Snowflake]]]):
        """|coro|
        Create a new channel object for the guild.

        Parameters
        ----------

        *channel : Dict[str, Optional[Union[int, bool, :class:`~pincer.utils.snowflake.Snowflake`]
            Keys:
                - id : :class:`~pincer.utils.snowflake.Snowflake`
                - position : Optional[int]
                - lock_permissions : Optional[bool]
                - parent_id : Optional[:class:`~pincer.utils.snowflake.Snowflake`]

        """

    async def list_active_threads(self) -> Tuple[
        List[Union[PublicThread, PrivateThread]], List[GuildMember]]:
        """|coro|
        Returns all active threads in the guild, including public and private threads.
        """
        data = await self._http.get(f"guilds/{self.id}/threads/active")

        threads = [Channel.from_dict(channel) for channel in data["threads"]]
        members = [GuildMember.from_dict(member) for member in data["members"]]

        return threads, members

    async def list_guild_members(self, limit: int = 1, after: int = 0):
        """|coro|
        Returns a list of guild member objects that are members of the guild.

        Parameters
        ----------
        limit : int
            max number of members to return (1-1000) |default| :data:`1`
        after : int
            the highest user id in the previous page |default| :data:`0`
        """

        return await self._http.get(
            f"guilds/{self.id}/members?limit={limit}&after={after}"
        )

    async def search_guild_members(self, query: str,
                                   limit: Optional[int] = None
                                   ) -> List[GuildMember]:
        """|coro|
        Returns a list of guild member objects whose username or nickname starts with a provided string.

        Parameters
        ----------
        query : str
            Query string to match username(s) and nickname(s) against.
        limit : Optional[int]
            max number of members to return (1-1000) |default| :data:`1`

        """

        data = await self._http.get(
            f"guilds/{id}/members/search?query={query}"
            f"&{limit}" if limit else ""
        )

        return [GuildMember.from_dict(member) for member in data]

    @overload
    async def add_guild_member(self, *, user_id: Snowflake,
                               access_token: str,
                               nick: Optional[str] = None,
                               roles: Optional[List[Snowflake]] = None,
                               mute: Optional[bool] = None,
                               deaf: Optional[bool] = None
                               ) -> Optional[GuildMember]:
        """|coro|
        Adds a user to the guild, provided you have a valid oauth2 access token for the user with the guilds.join scope.

        Parameters
        ----------
        user_id : str
            id of the user to be added
        access_token : str
            an oauth2 access token granted with the guilds.join to the bot's application for the user you want to add to the guild
        nick : Optional[str]
        	value to set users nickname to
        roles : Optional[List[:class:`~pincer.utils.snowflake.Snowflake`]]
        	array of role ids the member is assigned
        mute : Optional[bool]
        	whether the user is muted in voice channels
        deaf : Optional[bool]
        	whether the user is deafened in voice channels

        Returns
        -------
        :class:`~pincer.objects.guild.member.GuildMember`
            If the user is not in the guild
        None
            If the user is in the guild
        """

    async def add_guild_member(self, user_id, **kwargs):
        data = self._http.put(f"guilds/{self.id}/members/{user_id}",
                              data=kwargs)

        return GuildMember.from_dict(data) if data else None

    async def modify_current_member(self, nick: str) -> GuildMember:
        """|coro|
        Modifies the current member in a guild.

        Parameters
        ----------
        nick : str
            value to set users nickname to
        """
        data = self._http.patch(f"guilds/{self.id}/members/@me", {"nick": nick})
        member = GuildMember.from_dict(data)
        return member

    async def add_guild_member_role(self, user_id: int, role_id: int) -> None:
        """|coro|
        Adds a role to a guild member.

        Parameters
        ----------
        user_id : int
            id of the user to give a role to
        role_id : int
            id of a role
        """
        data = await self._http.put(
            f"guilds/{self.id}/{user_id}/roles/{role_id}", {})
        # TODO: remove the blank dictionary once #233 is fixed

    async def remove_guild_member_role(self, user_id: int,
                                       role_id: int) -> None:
        """|coro|
        Removes a role to a guild member.

        Parameters
        ----------
        user_id : int
            id of the user to remove a role from
        role_id : int
            id of a role
        """
        await self._http.delete(f"guilds/{self.id}/{user_id}/roles/{role_id}",
                                {})
        # TODO: remove the blank dictionary and format once #233 is fixed

    async def remove_guild_member(self, user_id: int) -> None:
        """|coro|
        Remove a member from a guild.

        Parameters
        ----------
        user_id : int
            id of the user to remove from the guild
        """
        await self._http.delete(f"guilds/{self.id}/members/{user_id}")

    async def kick(self, member_id: int, **kwargs):
        """|coro|
        Kicks a guild member.

        Parameters
        ----------
        member_id : :class: int
            ID of the guild member to kick.
        \\*\\* kwargs
            Additional keyword arguments to kick the guild member with.
        """
        await self._http.put(f"/guilds/{self.id}/bans/{member_id}", data=kwargs)

    async def ban(self, member_id: int):
        """|coro|
        Bans a guild member.

        Parameters
        ----------
        member_id : :class: int
            ID of the guild member to ban.
        """
        await self._http.delete(f"/guilds/{self.id}/members/{member_id}")

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
