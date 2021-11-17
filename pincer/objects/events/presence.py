# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING, APINullable

if TYPE_CHECKING:
    from typing import List, Optional, Tuple
    from ..user.user import User
    from ...utils.snowflake import Snowflake


class ActivityType(IntEnum):
    """Represents the enum of the type of activity.

    Attributes
    ----------
    GAME:
        Playing {name}; e.g. "Playing Rocket League"
    STREAMING:
        Streaming {details}; e.g. "Streaming Rocket League"; Only supports Twitch and YouTube.
    LISTENING:
        Listening to {name}; e.g. "Listening to Spotify"
    WATCHING:
        Watching {name}; e.g. "Watching YouTube Together"
    CUSTOM:
        \\{emoji} {name}; e.g. "\\:smiley: I am cool"; Not for bots; discord limitation
    COMPETING:
        Competing in {name}; e.g. "Competing in Arena World Champions"
    """
    # noqa: E501
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5


@dataclass
class ActivityTimestamp(APIObject):
    """Represents the timestamp of an activity.

    Attributes
    ----------
    start: APINullable[:class:`int`]
        Unix time (in milliseconds) of when the activity started
    end: APINullable[:class:`int`]
        Unix time (in milliseconds) of when the activity ends
    """
    start: APINullable[int] = MISSING
    end: APINullable[int] = MISSING


@dataclass
class ActivityEmoji(APIObject):
    """Represents an emoji in an activity.

    Attributes
    ----------
    name: :class:`str`
        The name of the emoji
    id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the emoji
    animated: APINullable[:class:`bool`]
        Whether this emoji is animated
    """
    name: str
    id: APINullable[Snowflake] = MISSING
    animated: APINullable[bool] = MISSING


@dataclass
class ActivityParty(APIObject):
    """Represents a party in an activity.

    Attributes
    ----------
    id: APINullable[:class:`str`]
        The id of the party
    size: APINullable[Tuple[:class:`int`, :class:`int`]]
        Array of two integers (current_size, max_size)
    """
    id: APINullable[str] = MISSING
    size: APINullable[Tuple[int, int]] = MISSING


@dataclass
class ActivityAssets(APIObject):
    """Represents an asset of an activity.

    Attributes
    ----------
    large_image: APINullable[:class:`str`]
        the id for a large asset of the activity, usually a snowflake
    large_text: APINullable[:class:`str`]
        text displayed when hovering over
        the large image of the activity
    small_image: APINullable[:class:`str`]
        the id for a small asset of the activity, usually a snowflake
    small_text: APINullable[:class:`str`]
        text displayed when hovering over
        the small image of the activity
    """
    large_image: APINullable[str] = MISSING
    large_text: APINullable[str] = MISSING
    small_image: APINullable[str] = MISSING
    small_text: APINullable[str] = MISSING


@dataclass
class ActivitySecrets(APIObject):
    """Represents a secret of an activity.

    Attributes
    ----------
    join: APINullable[:class:`str`]
        The secret for joining a party
    spectate: APINullable[:class:`str`]
        The secret for spectating a game
    match: APINullable[:class:`str`]
        The secret for a specific instanced match
    """
    join: APINullable[str] = MISSING
    spectate: APINullable[str] = MISSING
    match_: APINullable[str] = MISSING


class ActivityFlags(IntEnum):
    INSTANCE = 1 << 0
    JOIN = 1 << 1
    SPECTATE = 1 << 2
    JOIN_REQUEST = 1 << 3
    SYNC = 1 << 4
    PLAY = 1 << 5


@dataclass
class ActivityButton(APIObject):
    """When received over the gateway, the buttons field is an array
    of strings, which are the button labels. Bots cannot access
    a user's activity button URLs. When sending, the buttons field
    must be an array of this object.

    Attributes
    ----------
    label: :class:`str`
        The text shown on the button (1-32 characters)
    url: :class:`str`
        The url opened when clicking the button (1-512 characters)
    """
    label: str
    url: str


@dataclass
class Activity(APIObject):
    """Bots are only able to send ``name``, ``type``, and optionally ``url``.

    Attributes
    ----------
    name: :class:`str`
        The activity's name
    type: :class:`~pincer.objects.events.presence.ActivityType`
        Activity type
    created_at: :class:`int`
        Unix timestamp (in milliseconds) of when
        the activity was added to the user's session
    url: APINullable[Optional[:class:`str`]]
        Stream url, is validated when type is 1
    timestamps: APINullable[:class:`~pincer.objects.events.presence.ActivityTimestamp`]
        Unix timestamps for start and/or end of the game
    application_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Application id for the game
    details: APINullable[Optional[:class:`str`]]
        What the player is currently doing
    state: APINullable[Optional[:class:`str`]]
        The user's current party status
    emoji: APINullable[Optional[:class:`~pincer.objects.events.presence.ActivityEmoji`]]
        The emoji used for a custom status
    party: APINullable[:class:`~pincer.objects.events.presence.ActivityParty`]
        Information for the current party of the player
    assets: APINullable[:class:`~pincer.objects.events.presence.ActivityAssets`]
        Images for the presence and their hover texts
    secrets: APINullable[:class:`~pincer.objects.events.presence.ActivitySecrets`]
        Secrets for Rich Presence joining and spectating
    instance: APINullable[:class:`bool`]
        "nether or not the activity is an instanced game session
    flags: APINullable[:class:`~pincer.objects.events.presence.ActivityFlags`]
        Activity flags ``OR``\\d together,
        describes what the payload includes
    buttons: APINullable[List[:class:`~pincer.objects.events.presence.ActivityButton`]]
        The url button on an activity.
    """
    # noqa: E501
    name: str
    type: ActivityType
    created_at: int

    url: APINullable[Optional[str]] = MISSING
    timestamps: APINullable[ActivityTimestamp] = MISSING
    application_id: APINullable[Snowflake] = MISSING
    details: APINullable[Optional[str]] = MISSING
    state: APINullable[Optional[str]] = MISSING
    emoji: APINullable[Optional[ActivityEmoji]] = MISSING
    party: APINullable[ActivityParty] = MISSING
    assets: APINullable[ActivityAssets] = MISSING
    secrets: APINullable[ActivitySecrets] = MISSING
    instance: APINullable[bool] = MISSING
    flags: APINullable[ActivityFlags] = MISSING
    buttons: APINullable[List[ActivityButton]] = MISSING


@dataclass
class ClientStatus(APIObject):
    """Active sessions are indicated with an "online",
    "idle", or "dnd" string per platform.
    If a user is offline or invisible, the corresponding
    field is not present.

    Attributes
    ----------
    desktop: APINullable[:class:`str`]
        The user's status set for an active desktop
        (Windows, Linux, Mac) application session
    mobile: APINullable[:class:`str`]
        The user's status set for an active mobile
        (iOS, Android) application session
    web: APINullable[:class:`str`]
        The user's status set for an active web
        (browser, bot account) application session
    """
    desktop: APINullable[str] = MISSING
    mobile: APINullable[str] = MISSING
    web: APINullable[str] = MISSING


@dataclass
class PresenceUpdateEvent(APIObject):
    """This event is sent when a user's presence or info,
    such as name or avatar, is updated.

    Attributes
    ----------
    user: :class:`~pincer.objects.user.user.User`
        The user presence is being updated for
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild
    status: :class:`str`
        Either "idle", "dnd", "online", or "offline"
    activities: List[:class:`~pincer.objects.events.presence.Activity`]
        User's current activities
    client_status: :class:`~pincer.objects.events.presence.ClientStatus`
        User's platform-dependent status
    """
    user: User
    status: str
    activities: List[Activity]
    client_status: ClientStatus
    guild_id: APINullable[Snowflake] = MISSING
