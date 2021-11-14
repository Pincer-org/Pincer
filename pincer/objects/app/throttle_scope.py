# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from enum import Enum, auto


class ThrottleScope(Enum):
    """On what the cooldown should be set/on what should the cooldown be
    set.

    Attributes
    ----------
    GUILD:
        The cooldown is per guild.
    CHANNEL:
        The cooldown is per channel.
    USER:
        The cooldown is per user.
    GLOBAL:
        The cooldown is global.
    """
    GUILD = auto()
    CHANNEL = auto()
    USER = auto()
    GLOBAL = auto()
