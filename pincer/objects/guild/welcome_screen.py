# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake


@dataclass
class WelcomeScreenChannel(APIObject):
    """
    Represents a welcome screen channel. This is a channel which gets
    shown on the welcome screen.

    :param channel_id:
        the channel's id

    :param description:
        the description shown for the channel

    :param emoji_id:
        the emoji id, if the emoji is custom

    :param emoji_name:
        the emoji name if custom, the unicode character if standard,
        or null if no emoji is set
    """

    channel_id: Snowflake
    description: str

    emoji_id: Optional[int] = None
    emoji_name: Optional[str] = None


@dataclass
class WelcomeScreen(APIObject):
    """
    Representation of a Discord guild/server welcome screen.

    :description:
        the server description shown in the welcome screen

    :welcome_channels:
        the channels shown in the welcome screen, up to 5
    """
    welcome_channels: List[WelcomeScreenChannel]

    description: Optional[str] = None
