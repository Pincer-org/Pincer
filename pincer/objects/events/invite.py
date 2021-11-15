# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import APINullable, MISSING

if TYPE_CHECKING:
    from ..user.user import User
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp
    from ..guild.invite import InviteTargetType


@dataclass
class InviteCreateEvent(APIObject):
    """Sent when a new invite to a channel is created.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The channel the invite is for
    code: :class:`str`
        The unique invite code
    created_at: :class:`~pincer.utils.timestamp.Timestamp`
        The time at which the invite was created
    max_age: :class:`int`
        How long the invite is valid for (in seconds)
    max_uses: :class:`int`
        The maximum number of times the invite can be used
    temporary: :class:`bool`
        Whether or not the invite is temporary (invited users will
        be kicked on disconnect unless they're assigned a role)
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The guild of the invite
    inviter: APIObject[:class:`~pincer.objects.user.user.User`]
        The user that created the invite
    target_type: APINullable[:class:`~pincer.objects.guild.invite.InviteTargetType`]
        The type of target for this voice channel invite
    target_user: APINullable[:class:`~pincer.objects.user.user.User`]
        The user whose stream to display for
        this voice channel stream invite
    uses: :class:`int`
        How many times the invite has been used (always will be ``0``)
    """
    # noqa: E501
    channel_id: Snowflake
    code: str
    created_at: Timestamp
    max_age: int
    max_uses: int
    temporary: bool

    guild_id: APINullable[Snowflake] = MISSING
    inviter: APINullable[User] = MISSING
    target_type: APINullable[InviteTargetType] = MISSING
    target_user: APINullable[User] = MISSING
    uses: int = 0


@dataclass
class InviteDeleteEvent(APIObject):
    """Sent when an invite is deleted.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The channel of the invite
    code: :class:`str`
        The unique invite code
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The guild of the invite
    """
    channel_id: Snowflake
    code: str

    guild_id: APINullable[Snowflake] = MISSING
