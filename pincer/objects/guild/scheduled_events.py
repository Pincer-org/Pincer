# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, TYPE_CHECKING

from ...utils.api_object import APIObject, MISSING

if TYPE_CHECKING:
    from ..guild.stage import PrivacyLevel
    from ..guild.member import GuildMember
    from ..user.user import User
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp
    from ...utils.types import APINullable


class EventStatus(IntEnum):
    """
    The status of an event.

    Attributes
    ----------
    SCHEDULED: int
        The event is scheduled.
    ACTIVE: int
        The event is active.
    CANCELLED: int
        The event is cancelled.
    COMPLETED: int
        The event is completed.
    """

    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3
    CANCELLED = 4


class GuildScheduledEventEntityType(IntEnum):
    """
    The type of entity that is scheduled.

    Attributes
    ----------
    STAGE_INSTANCE: int
        The event is scheduled for a stage instance.
    VOICE: int
        The event is scheduled for a voice channel.
    EXTERNAL: int
        The event is scheduled for an external resource.
    """

    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3


@dataclass(repr=False)
class ScheduledEvent(APIObject):
    """
    Represents a scheduled event in a guild.

    Attributes
    ----------
    id: :class:`int`
        The ID of the scheduled event.
    name: :class:`str`
        The name of the scheduled event (1-100 characters)
    guild_id: :class:`int`
        The guild id which the scheduled event belongs to
    scheduled_start_time: str
        The scheduled start time of the event.
    privacy_level: :class:`~pincer.guild.stage.PrivacyLevel`
        The privacy level of the scheduled event.
    status: :class:`~pincer.guild.schedule_events.EventStatus`
        The status of the scheduled event.
    entity_type: :class:`~pincer.guild.schedule_events.GuildScheduledEventEntityType`
        The type of the scheduled event
    channel_id: APINullable[:class:`int`]
        The channel id in which the scheduled event will be hosted,
        or null if scheduled entity type is EXTERNAL
    creator_id: APINullable[:class:`int`]
        The user id of the creator of the scheduled event
    scheduled_end_time: str
        The time the scheduled event will end, required if entity_type is EXTERNAL
    description: APINullable[:class:`str`]
        The description of the scheduled event (0-1000 characters)
    entity_id: APINullable[:class:`int`]
        The id of an entity associated with a guild scheduled event
    entity_metadata: APINullable[:class:`str`]
        Additional metadata for the guild scheduled event
    creator: APINullable[:class:`~pincer.objects.user.user.User`]
        The user who created the scheduled event
    user_count: APINullable[:class:`int`]
        The number of users who have joined the scheduled event
    """

    id: Snowflake
    name: str
    guild_id: Snowflake
    scheduled_start_time: Timestamp
    privacy_level: PrivacyLevel
    status: EventStatus
    entity_type: GuildScheduledEventEntityType

    channel_id: APINullable[Snowflake] = MISSING
    creator_id: APINullable[Snowflake] = MISSING
    scheduled_end_time: Optional[Timestamp] = None

    description: APINullable[str] = MISSING
    entity_id: APINullable[Snowflake] = MISSING
    entity_metadata: APINullable[str] = MISSING
    creator: APINullable[User] = MISSING
    user_count: APINullable[int] = MISSING


@dataclass
class GuildScheduledEventUser(APIObject):
    """
    Represents a user who has joined a scheduled event.

    Attributes
    ----------
    guild_scheduled_event_id: :class:`int`
        the scheduled event id which the user subscribed to
    user : :class:`~pincer.objects.user.user.User`
        user which subscribed to an event
    member : APINullable[:class:`~pincer.objects.guild.member.GuildMember`]
                guild member data for this user for the guild which this event belongs to, if any
    """

    guild_scheduled_event_id: Snowflake
    user: User
    member: APINullable[GuildMember] = MISSING
