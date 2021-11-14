# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Optional, List

    from ...utils.snowflake import Snowflake


@dataclass
class WelcomeScreenChannel(APIObject):
    """Represents a welcome screen channel. This is a channel which gets
    shown on the welcome screen.

    Attributes
    ----------
    channel_id: :class:`~pincer.utils.snowflake.Snowflake`
        The channel's id
    description: :class:`str`
        The description shown for the channel
    emoji_id: Optional[:class:`int`]
        The emoji id, if the emoji is custom
    emoji_name: Optional[:class:`str`]
        The emoji name if custom, the unicode character if standard,
        or null if no emoji is set
    """
    channel_id: Snowflake
    description: str

    emoji_id: Optional[int] = None
    emoji_name: Optional[str] = None


@dataclass
class WelcomeScreen(APIObject):
    """Representation of a Discord guild/server welcome screen.

    Attributes
    ----------
    description: LIst[:class:`~pincer.objects.guild.welcome_screen.WelcomeScreenChannel`]
        The server description shown in the welcome screen
    welcome_channels: Optional[:class:`str`]
        The channels shown in the welcome screen, up to 5
    """  # noqa: E501
    welcome_channels: List[WelcomeScreenChannel]

    description: Optional[str] = None
