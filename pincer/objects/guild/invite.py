# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, List, TYPE_CHECKING

from ..app import application
from ..guild.channel import Channel
from ...utils.api_object import APIObject
from ...utils.types import MISSING
from ...utils import types
from . import guild
from ..user.user import User
from ..guild.member import GuildMember
from ...utils.timestamp import Timestamp


class InviteTargetType(IntEnum):
    """
    Represents the type of the invite.

    :param STREAM:
        A normal Discord invite, eg for a channel or guild.

    :param EMBEDDED_APPLICATION:
        An embedded application invite, eg poker-night etc
    """
    STREAM = 1
    EMBEDDED_APPLICATION = 2


@dataclass
class InviteStageInstance(APIObject):
    """
    Represents an invite for a Discord stages channel.

    :param members:
        the members speaking in the Stage

    :param participant_count:
        the number of users in the Stage

    :param speaker_count:
        the number of users speaking in the Stage

    :param topic:
        the topic of the Stage instance (1-120 characters)
    """

    members: List[GuildMember]
    participant_count: int
    speaker_count: int
    topic: str


@dataclass
class InviteMetadata(APIObject):
    """
    Extra information about an invite, will extend the invite object.

    :param uses:
        number of times this invite has been used

    :param max_uses:
        max number of times this invite can be used

    :param max_age:
        duration (in seconds) after which the invite expires

    :param temporary:
        whether this invite only grants temporary membership

    :param created_at:
        when this invite was created
    """
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: Timestamp


@dataclass
class Invite(APIObject):
    """
    Represents a Discord invite.

    :param channel:
        the channel this invite is for

    :param code:
        the invite code (unique ID)

    :param approximate_member_count:
        approximate count of total members, returned from the GET
        /invites/<code> endpoint when with_counts is true

    :param approximate_presence_count:
        approximate count of online members, returned from the GET
        /invites/<code> endpoint when with_counts is true

    :param expires_at:
        the expiration date of this invite, returned from the GET
        /invites/<code> endpoint when with_expiration is true

    :param inviter:
        the user who created the invite

    :param guild:
        the guild this invite is for

    :param stage_instance:
        stage instance data if there is a public Stage instance in the Stage
        channel this invite is for

    :param target_type:
        the type of target for this voice channel invite

    :param target_user:
        the user whose stream to display for this voice channel stream invite

    :param target_application:
        the embedded application to open for this voice channel embedded
        application invite
    """

    channel: Channel
    code: str

    approximate_member_count: types.APINullable[int] = MISSING
    approximate_presence_count: types.APINullable[int] = MISSING
    expires_at: types.APINullable[Optional[Timestamp]] = MISSING
    inviter: types.APINullable[User] = MISSING
    guild: types.APINullable[guild.Guild] = MISSING
    stage_instance: types.APINullable[InviteStageInstance] = MISSING
    target_type: types.APINullable[InviteTargetType] = MISSING
    target_user: types.APINullable[User] = MISSING
    target_application: types.APINullable[application.Application] = MISSING
