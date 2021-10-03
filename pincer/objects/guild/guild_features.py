# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import Enum, auto


class GuildFeatures(Enum):
    """Represents Guild Features strings."""
    ANIMATED_ICON = auto()
    BANNER = auto()
    COMMERCE = auto()
    COMMUNITY = auto()
    DISCOVERABLE = auto()
    FEATURABLE = auto()
    INVITE_SPLASH = auto()
    MEMBER_VERIFICATION_GATE_ENABLED = auto()
    NEWS = auto()
    PARTNERED = auto()
    PREVIEW_ENABLED = auto()
    VANITY_URL = auto()
    VERIFIED = auto()
    VIP_REGIONS = auto()
    WELCOME_SCREEN_ENABLED = auto()
    TICKETED_EVENTS_ENABLED = auto()
    MONETIZATION_ENABLED = auto()
    MORE_STICKERS = auto()
    THREE_DAY_THREAD_ARCHIVE = auto()
    SEVEN_DAY_THREAD_ARCHIVE = auto()
    PRIVATE_THREADS = auto()
