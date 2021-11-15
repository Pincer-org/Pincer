# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import List, Optional

    from .guild import Guild
    from ..app.application import Application
    from ..guild.channel import Channel
    from ..guild.member import GuildMember
    from ..user.user import User
    from ...utils.timestamp import Timestamp
    from ...utils.types import APINullable


class InviteTargetType(IntEnum):
    """Represents the type of the invite.

    Attributes
    ----------
    STREAM:
        A normal Discord invite, eg for a channel or guild.
    EMBEDDED_APPLICATION:
        An embedded application invite, eg poker-night etc.
    """
    STREAM = 1
    EMBEDDED_APPLICATION = 2


@dataclass
class InviteStageInstance(APIObject):
    """Represents an invite for a Discord stages channel.

    Attributes
    ----------
    members: List[:class:`~pincer.objects.guild.member.GuildMember`]
        the members speaking in the Stage
    participant_count: :class:`int`
        the number of users in the Stage
    speaker_count: :class:`int`
        the number of users speaking in the Stage
    topic: :class:`str`
        the topic of the Stage instance (1-120 characters)
    """
    members: List[GuildMember]
    participant_count: int
    speaker_count: int
    topic: str


@dataclass
class InviteMetadata(APIObject):
    """Extra information about an invite, will extend the invite object.

    Attributes
    ----------
    uses: :class:`int`
        number of times this invite has been used
    max_uses: :class:`int`
        Max number of times this invite can be used
    max_age: :class:`int`
        Duration (in seconds) after which the invite expires
    temporary:  :class:`bool`
        Whether this invite only grants temporary membership
    created_at: :class:`~pincer.utils.timestamp.Timestamp`
        When this invite was created
    """
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: Timestamp


@dataclass
class Invite(APIObject):
    """Represents a Discord invite.

    Attributes
    ----------
    channel: :class:`~pincer.objects.guild.channel.Channel`
        The channel this invite is for
    code: :class:`str`
        The invite code (unique ID)
    approximate_member_count: APINullable[:class:`int`]
        Approximate count of total members, returned from the GET
        /invites/<code> endpoint when with_counts is true
    approximate_presence_count: APINullable[:class:`int`]
        Approximate count of online members, returned from the GET
        /invites/<code> endpoint when with_counts is true
    expires_at: APINullable[Optional[:class:`~pincer.utils.timestamp.Timestamp`]]
        The expiration date of this invite, returned from the GET
        /invites/<code> endpoint when with_expiration is true
    inviter: APINullable[:class:`~pincer.objects.user.user.User`]
        The user who created the invite
    guild: :class:`~pincer.objects.guild.guild.Guild`
        The guild this invite is for
    stage_instance: :class:`~pincer.objects.guild.invite.InviteStageInstance`
        Stage instance data if there is a public Stage instance in the Stage
        channel this invite is for
    target_type: :class:`~pincer.objects.guild.invite.InviteTargetType`
        The type of target for this voice channel invite
    target_user: :class:`~pincer.objects.user.user.User`
        The user whose stream to display for this voice channel stream invite
    target_application: :class:`~pincer.objects.app.application.Application`
        The embedded application to open for this voice channel embedded
        application invite
    """
    # noqa: E501

    channel: Channel
    code: str

    approximate_member_count: APINullable[int] = MISSING
    approximate_presence_count: APINullable[int] = MISSING
    expires_at: APINullable[Optional[Timestamp]] = MISSING
    inviter: APINullable[User] = MISSING
    guild: APINullable[Guild] = MISSING
    stage_instance: APINullable[InviteStageInstance] = MISSING
    target_type: APINullable[InviteTargetType] = MISSING
    target_user: APINullable[User] = MISSING
    target_application: APINullable[Application] = MISSING

    def __str__(self) -> str:
        return self.link

    @property
    def link(self):
        return f"https://discord.gg/{self.code}"
