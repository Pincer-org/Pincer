# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Optional

from ...utils.api_object import APIObject, ChannelProperty, GuildProperty

if TYPE_CHECKING:
    from ...client import Client
    from ...utils.snowflake import Snowflake


class PrivacyLevel(IntEnum):
    """Represents the level of publicity of a stage.

    Attributes
    ----------
    PUBLIC:
        The stage is public.
    GUILD_ONLY:
        The stage of for guild members only.
    """

    PUBLIC = 1
    GUILD_ONLY = 2


@dataclass(repr=False)
class StageInstance(APIObject, ChannelProperty, GuildProperty):
    """Represents a Stage Instance object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of this Stage instance
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Guild id of the associated Stage channel
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the associated Stage channel
    topic: :class:`str`
        Topic of the Stage instance (1-120 characters)
    privacy_level: :class:`~pincer.objects.guild.stage.PrivacyLevel`
        Privacy level of the Stage instance
    discoverable: :class:`bool`
        Is Stage Discovery enabled
    """

    id: Snowflake
    guild_id: Snowflake
    channel_id: Snowflake
    topic: str
    privacy_level: PrivacyLevel
    discoverable: bool

    @classmethod
    async def from_id(cls, client: Client, _id: int) -> StageInstance:
        return client.http.get(f"stage-instance/{_id}")

    async def modify(
        self,
        topic: Optional[str] = None,
        privacy_level: Optional[PrivacyLevel] = None,
        reason: Optional[str] = None,
    ):
        """|coro|
        Updates fields of an existing Stage instance.
        Requires the user to be a moderator of the Stage channel.

        Parameters
        ----------
        topic : Optional[:class:`str`]
            The topic of the Stage instance (1-120 characters)
        privacy_level : Optional[:class:`~pincer.objects.guild.stage.PrivacyLevel`]
            The privacy level of the Stage instance
        reason : Optional[:class:`str`]
            The reason for the modification
        """

        await self._client.modify_stage(self.id, topic, privacy_level, reason)
