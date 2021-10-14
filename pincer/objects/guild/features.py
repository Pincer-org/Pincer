# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import Enum, auto


class GuildFeatures(Enum):
    """Represents Guild Features strings.
    """
    ANIMATED_ICON = auto() #: Guild can have an animated icon.
    BANNER = auto() #: Guild can have a banner.
    COMMERCE = auto() #: Guild can have commerce.
    COMMUNITY = auto() #: Guild is a community.
    DISCOVERABLE = auto() #: Guild can be discovered.
    FEATURABLE = auto() #: Guild can be featureurable.
    INVITE_SPLASH = auto() #: Guild can have an invite splash.
    MEMBER_VERIFICATION_GATE_ENABLED = auto() #: Guild has member verification enabled.
    NEWS = auto() #: Guild has a news channel.
    PARTNERED = auto() #: Guild is a partner.
    PREVIEW_ENABLED = auto() #: Guild has preview enabled.
    VANITY_URL = auto() #: Guild has a vanity url.
    VERIFIED = auto() #: Guild is verified.
    VIP_REGIONS = auto() #: Guild can have VIP regions.
    WELCOME_SCREEN_ENABLED = auto() #: Guild has welcome screen enabled.
    TICKETED_EVENTS_ENABLED = auto() #: Guild has ticketed events enabled.
    MONETIZATION_ENABLED = auto() #: Guild has monetization enabled.
    MORE_STICKERS = auto() #: GUild can have more stickers.
    THREE_DAY_THREAD_ARCHIVE = auto() #: Guild can have three day archive time for threads.
    SEVEN_DAY_THREAD_ARCHIVE = auto() #: Guild can have seven day archive time for threads.
    PRIVATE_THREADS = auto() #: Guild can have private threads.
