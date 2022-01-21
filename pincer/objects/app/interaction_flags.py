# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from enum import IntFlag


class InteractionFlags(IntFlag):
    """

    Attributes
    ----------
    EPHEMERAL:
        only the user receiving the message can see it
    """
    EPHEMERAL = 1 << 6
