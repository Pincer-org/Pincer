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
    ANIMATED_ICON = "ANIMATED_ICON"
    BANNER = "BANNER"
    COMMERCE = "COMMERCE"
    COMMUNITY = "COMMUNITY"
    DISCOVERABLE = "DISCOVERABLE"
    FEATURABLE = "FEATURABLE"
    INVITE_SPLASH = "INVITE_SPLASH"
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    NEWS = "NEWS"
    PARTNERED = "PARTNERED"
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    VANITY_URL = "VANITY_URL"
    VERIFIED = "VERIFIED"
    VIP_REGIONS = "VIP_REGIONS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"
    TICKETED_EVENTS_ENABLED = "TICKETED_EVENTS_ENABLED"
    MONETIZATION_ENABLED = "MONETIZATION_ENABLED"
    MORE_STICKERS = "MORE_STICKERS"
    THREE_DAY_THREAD_ARCHIVE = "THREE_DAY_THREAD_ARCHIVE"
    SEVEN_DAY_THREAD_ARCHIVE = "SEVEN_DAY_THREAD_ARCHIVE"
    PRIVATE_THREADS = "PRIVATE_THREADS"
    NEW_THREAD_PERMISSIONS = "NEW_THREAD_PERMISSIONS"
