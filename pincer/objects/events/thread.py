# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import APINullable, MISSING

if TYPE_CHECKING:
    from typing import List

    from ..guild.channel import Channel
    from ..guild.thread import ThreadMember
    from ...utils.snowflake import Snowflake


@dataclass
class ThreadListSyncEvent(APIObject):
    """Sent when the current user gains access to a channel.

    Attributes
    ----------
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the guild
    threads: List[:class:`~pincer.objects.guild.channel.Channel`]
        All active threads in the given channels that
        the current user can access
    members: List[:class:`~pincer.objects.guild.thread.ThreadMember`]
        All thread member objects from the synced threads for
        the current user, indicating which threads the current
        user has been added to
    channel_ids: APINullable[List[:class:`~pincer.utils.snowflake.Snowflake`]]
        The parent channel ids whose threads are being synced.
        If omitted, then threads were synced for the entire guild.
        This array may contain channel_ids that have no active
        threads as well, so you know to clear that data.
    """
    guild_id: Snowflake
    threads: List[Channel]
    members: List[ThreadMember]

    channel_ids: APINullable[List[Snowflake]] = MISSING


@dataclass
class ThreadMembersUpdateEvent(APIObject):
    """Sent when anyone is added to or removed from a thread.
    If the current user does not have the `GUILD_MEMBERS`
    Gateway Intent, then this event will only be sent if
    the current user was added to or removed from the thread.

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the thread
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of the guild
    member_count: :class:`int`
        The approximate number of members in the thread, capped at 50
    added_members: APINullable[List[:class:`~pincer.objects.guild.thread.ThreadMember`]]
        The users who were added to the thread
    removed_member_ids: APINullable[List[:class:`~pincer.utils.snowflake.Snowflake`]]
        The id of the users who were removed from the thread
    """
    # noqa: E501
    id: Snowflake
    guild_id: Snowflake
    member_count: int

    added_members: APINullable[List[ThreadMember]] = MISSING
    removed_member_ids: APINullable[List[Snowflake]] = MISSING
