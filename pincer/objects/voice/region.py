# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...utils.api_object import APIObject


@dataclass
class VoiceRegion(APIObject):
    """Represents a Discord Voice Region object

    Attributes
    ----------
    id: :class:`str`
        Unique ID for the region
    name: :class:`str`
        Name of the region
    vip: :class:`bool`
        True if this is a vip-only server
    optimal: :class:`bool`
        True for a single server
        that is closest to the current user's client
    deprecated: :class:`bool`
        Whether this is a deprecated voice region
        (avoid switching to these)
    custom: :class:`bool`
        Whether this is a custom voice region
        (used for events/etc)
    """
    id: str
    name: str
    vip: bool
    optimal: bool
    deprecated: bool
    custom: bool
