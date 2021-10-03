# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...utils.api_object import APIObject


@dataclass
class VoiceRegion(APIObject):
    """
    Represents a Discord Voice Region object

    :param id:
        unique ID for the region

    :param name:
        name of the region

    :param vip:
        true if this is a vip-only server

    :param optimal:
        true for a single server
        that is closest to the current user's client

    :param deprecated:
        whether this is a deprecated voice region
        (avoid switching to these)

    :param custom:
        whether this is a custom voice region
        (used for events/etc)
    """
    id: str
    name: str
    vip: bool
    optimal: bool
    deprecated: bool
    custom: bool
