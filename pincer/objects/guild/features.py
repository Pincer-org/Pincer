# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import Enum


class GuildFeature(Enum):
    """Represents Guild Features strings.

    Attributes
    ----------
    ANIMATED_ICON : str
        Guild can have an animated icon.
    BANNER : str
        Guild can have a banner.
    COMMERCE : str
        Guild can have commerce.
    COMMUNITY : str
        Guild is a community.
    DISCOVERABLE : str
        Guild can be discovered.
    FEATURABLE : str
        Guild can be featureurable.Guild can have an invite splash.
    INVITE_SPLASH : str
        Guild can be featureurable.
    MEMBER_VERIFICATION_GATE_ENABLED : str
        Guild has member verification enabled.
    NEWS : str
        Guild has a news channel.
    PARTNERED : str
        Guild is a partner.
    PREVIEW_ENABLED : str
        Guild has preview enabled.
    VANITY_URL : str
        Guild has a vanity url.
    VERIFIED : str
        Guild is verified.
    VIP_REGIONS : str
        Guild can have VIP regions.
    WELCOME_SCREEN_ENABLED : str
        Guild has welcome screen enabled.
    TICKETED_EVENTS_ENABLED : str
        Guild has ticketed events enabled.
    MONETIZATION_ENABLED : str
        Guild has monetization enabled.
    MORE_STICKERS : str
        Guild can have more stickers.
    THREE_DAY_THREAD_ARCHIVE : str
        Guild can have three day archive time for threads.
    SEVEN_DAY_THREAD_ARCHIVE : str
        Guild can have seven day archive time for threads.
    PRIVATE_THREADS : str
        Guild can have private threads.
    THREADS_ENABLED : str
        Guild can have threads enabled.
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
    THREADS_ENABLED = "THREADS_ENABLED"
    ROLE_ICONS = "ROLE_ICONS"
    ANIMATED_BANNER = "ANIMATED_BANNER"
    MEMBER_PROFILES = "MEMBER_PROFILES"
    ENABLED_DISCOVERABLE_BEFORE = "ENABLED_DISCOVERABLE_BEFORE"
