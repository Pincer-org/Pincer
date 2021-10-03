# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional, Tuple

from ..user import User
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING, APINullable


class ActivityType(IntEnum):
    """
    :param GAME:
        Playing {name}
        e.g. "Playing Rocket League"

    :param STREAMING:
        Streaming {details}
        e.g. "Streaming Rocket League"
        Only supports Twitch and YouTube.

    :param LISTENING:
        Listening to {name}
        e.g. "Listening to Spotify"

    :param WATCHING:
        Watching {name}
        e.g. "Watching YouTube Together"

    :param CUSTOM:
        {emoji} {name}
        e.g. ":smiley: I am cool"

    :param COMPETING:
        Competing in {name}
        e.g. "Competing in Arena World Champions"
    """
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5


@dataclass
class ActivityTimestamp(APIObject):
    """
    :param start:
        unix time (in milliseconds) of when the activity started

    :param end:
        unix time (in milliseconds) of when the activity ends
    """
    start: APINullable[int] = MISSING
    end: APINullable[int] = MISSING


@dataclass
class ActivityEmoji(APIObject):
    """
    :param name:
        the name of the emoji

    :param id:
        the id of the emoji

    :param animated:
        whether this emoji is animated
    """
    name: str
    id: APINullable[Snowflake] = MISSING
    animated: APINullable[bool] = MISSING


@dataclass
class ActivityParty(APIObject):
    """
    :param id:
        the id of the party

    :param size:
        array of two integers (current_size, max_size)
    """
    id: APINullable[str] = MISSING
    size: APINullable[Tuple[int, int]] = MISSING


@dataclass
class ActivityAssets(APIObject):
    """
    :param large_image:
        the id for a large asset of the activity, usually a snowflake

    :param large_text:
        text displayed when hovering over
        the large image of the activity

    :param small_image:
        the id for a small asset of the activity, usually a snowflake

    :param small_text:
        text displayed when hovering over
        the small image of the activity
    """
    large_image: APINullable[str] = MISSING
    large_text: APINullable[str] = MISSING
    small_image: APINullable[str] = MISSING
    small_text: APINullable[str] = MISSING


@dataclass
class ActivitySecrets(APIObject):
    """
    :param join:
        the secret for joining a party

    :param spectate:
        the secret for spectating a game

    :param match:
        the secret for a specific instanced match
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
    """
    When received over the gateway, the buttons field is an array
    of strings, which are the button labels. Bots cannot access
    a user's activity button URLs. When sending, the buttons field
    must be an array of this object.

    :param label:
        the text shown on the button (1-32 characters)

    :param url:
        the url opened when clicking the button (1-512 characters)
    """
    label: str
    url: str


@dataclass
class Activity(APIObject):
    """
    Bots are only able to send `name`, `type`, and optionally `url`.

    :param name:
        the activity's name

    :param type:
        activity type

    :param url:
        stream url, is validated when type is 1

    :param created_at:
        unix timestamp (in milliseconds) of when
        the activity was added to the user's session

    :param timestamps:
        unix timestamps for start and/or end of the game

    :param application_id:
        application id for the game

    :param details:
        what the player is currently doing

    :param state:
        the user's current party status

    :param emoji:
        the emoji used for a custom status

    :param party:
        information for the current party of the player

    :param assets:
        images for the presence and their hover texts

    :param secrets:
        secrets for Rich Presence joining and spectating

    :param instance:
        whether or not the activity is an instanced game session

    :param flags:
        activity flags `OR`d together,
        describes what the payload includes
    """
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
    """
    Active sessions are indicated with an "online",
    "idle", or "dnd" string per platform.
    If a user is offline or invisible, the corresponding
    field is not present.

    :param desktop:
        the user's status set for an active desktop
        (Windows, Linux, Mac) application session

    :param mobile:
        the user's status set for an active mobile
        (iOS, Android) application session

    :param web:
        the user's status set for an active web
        (browser, bot account) application session
    """
    desktop: APINullable[str] = MISSING
    mobile: APINullable[str] = MISSING
    web: APINullable[str] = MISSING


@dataclass
class PresenceUpdateEvent(APIObject):
    """
    This event is sent when a user's presence or info,
    such as name or avatar, is updated.

    :param user:
        the user presence is being updated for

    :param guild_id:
        id of the guild

    :param status:
        either "idle", "dnd", "online", or "offline"

    :param activities:
        user's current activities

    :param client_status:
        user's platform-dependent status
    """
    user: User
    guild_id: Snowflake
    status: str
    activities: List[Activity]
    client_status: ClientStatus
