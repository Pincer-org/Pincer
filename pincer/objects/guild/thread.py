# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass

from ...utils.api_object import APIObject
from ...utils.types import MISSING
from ...utils import types, snowflake, timestamp


@dataclass
class ThreadMetadata(APIObject):
    """
    Represents a Discord Thread Metadata object

    :param archived:
        whether the thread is archived

    :param auto_archive_duration:
        duration in minutes to automatically archive the thread
        after recent activity, can be set to: 60, 1440, 4320, 10080

    :param archive_timestamp:
        timestamp when the thread's archive status was last changed,
        used for calculating recent activity

    :param locked:
        whether the thread is locked; when a thread is locked,
        only users with MANAGE_THREADS can unarchive it

    :param invitable:
        whether non-moderators can add other non-moderators to a thread;
        only available on private threads
    """
    archived: bool
    auto_archive_duration: int
    archive_timestamp: timestamp.Timestamp
    locked: bool

    invitable: types.APINullable[bool] = MISSING


@dataclass
class ThreadMember(APIObject):
    """
    Represents a Discord Thread Member object

    :param join_timestamp:
        the time the current user last joined the thread

    :param flags:
        any user-thread settings, currently only used for notifications

    :param id:
        id of the thread

    :param user_id:
        id of the user
    """
    join_timestamp: timestamp.Timestamp
    flags: int

    id: types.APINullable[snowflake.Snowflake] = MISSING
    user_id: types.APINullable[snowflake.Snowflake] = MISSING
