# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from enum import Enum, auto


class ThrottleScope(Enum):
    """
    On what the cooldown should be set/on what should the cooldown be
    set.

    :param GUILD:
        The cooldown is per guild.

    :param CHANNEL:
        The cooldown is per channel.

    :param USER:
        The cooldown is per user.

    :param GLOBAL:
        The cooldown is global.
    """
    GUILD = auto()
    CHANNEL = auto()
    USER = auto()
    GLOBAL = auto()
