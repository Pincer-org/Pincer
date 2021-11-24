# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass

from ...utils.api_object import APIObject
from ...utils.types import MISSING


@dataclass
class Mentionable(APIObject):
    user = MISSING
    role = MISSING
