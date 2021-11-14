# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp


@dataclass
class ThreadMetadata(APIObject):
    """
    Represents a Discord Thread Metadata object

    Attributes
    ----------
    archived: :class:`bool`
        Whether the thread is archived
    auto_archive_duration: :class:`int`
        Duration in minutes to automatically archive the thread
        after recent activity, can be set to: 60, 1440, 4320, 10080
    archive_timestamp: :class:`~pincer.utils.timestamp.Timestamp`
        Timestamp when the thread's archive status was last changed,
        used for calculating recent activity
    locked: :class:`bool`
        Whether the thread is locked; when a thread is locked,
        only users with MANAGE_THREADS can unarchive it
    invitable: APINullable[:class:`bool`]
        Whether non-moderators can add other non-moderators to a thread;
        only available on private threads
    """
    archived: bool
    auto_archive_duration: int
    archive_timestamp: Timestamp
    locked: bool

    invitable: APINullable[bool] = MISSING


@dataclass
class ThreadMember(APIObject):
    """Represents a Discord Thread Member object

    Attributes
    ----------
    join_timestamp: :class:`~pincer.utils.timestamp.Timestamp`
        The time the current user last joined the thread
    flags: :class:`int`
        Any user-thread settings, currently only used for notifications
    id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the thread
    user_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the user
    """
    join_timestamp: Timestamp
    flags: int

    id: APINullable[Snowflake] = MISSING
    user_id: APINullable[Snowflake] = MISSING
