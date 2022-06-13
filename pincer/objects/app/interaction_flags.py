# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from enum import IntFlag


class InteractionFlags(IntFlag):
    """

    Attributes
    ----------
    EPHEMERAL:
        Only the user receiving the message can see it.
    SUPPRESS_EMBEDS:
        No link embeds should be shown for this message.
    """

    EPHEMERAL = 1 << 6
    SUPPRESS_EMBEDS = 1 << 2
