# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import Enum, auto


class GuildFeature(Enum):
    """Represents Guild Features strings.

    Attributes
    ----------
    ANIMATED_ICON:
        Guild can have an animated icon.
    BANNER:
        Guild can have a banner.
    COMMERCE:
        Guild can have commerce.
    COMMUNITY:
        Guild is a community.
    DISCOVERABLE:
        Guild can be discovered.
    FEATURABLE:
        Guild can be featureurable.Guild can have an invite splash.
    INVITE_SPLASH:
        Guild can be featureurable.
    MEMBER_VERIFICATION_GATE_ENABLED:
        Guild has member verification enabled.
    NEWS:
        Guild has a news channel.
    PARTNERED:
        Guild is a partner.
    PREVIEW_ENABLED:
        Guild has preview enabled.
    VANITY_URL:
        Guild has a vanity url.
    VERIFIED:
        Guild is verified.
    VIP_REGIONS:
        Guild can have VIP regions.
    WELCOME_SCREEN_ENABLED:
        Guild has welcome screen enabled.
    TICKETED_EVENTS_ENABLED:
        Guild has ticketed events enabled.
    MONETIZATION_ENABLED:
        Guild has monetization enabled.
    MORE_STICKERS:
        Guild can have more stickers.
    THREE_DAY_THREAD_ARCHIVE:
        Guild can have three day archive time for threads.
    SEVEN_DAY_THREAD_ARCHIVE:
        Guild can have seven day archive time for threads.
    PRIVATE_THREADS:
        Guild can have private threads.
    """
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
