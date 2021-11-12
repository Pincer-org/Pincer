# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from enum import IntEnum


class InteractionFlags(IntEnum):
    """

    Attributes
    ----------
    EPHEMERAL:
        only the user receiving the message can see it
    """
    EPHEMERAL = 1 << 6
