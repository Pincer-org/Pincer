# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from enum import Enum, auto


class ThrottleScope(Enum):
    """On what the cooldown should be set/on what should the cooldown be
    set.
    """
    GUILD = auto()  #: The cooldown is per guild.
    CHANNEL = auto()  #: The cooldown is per channel.
    USER = auto()  #: The cooldown is per user.
    GLOBAL = auto()  #: The cooldown is global.
