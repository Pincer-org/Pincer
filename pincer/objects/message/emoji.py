# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake
from ...utils.types import MISSING
from ...utils import types
from ..guild.role import Role
from ..user.user import User


@dataclass
class Emoji(APIObject):
    """
    :param id:
        emoji id

    :param name:
        emoji name

    :param animated:
        whether this emoji is animated

    :param available:
        whether this emoji can be used, may be false due to loss of Server
        Boosts

    :param managed:
        whether this emoji is managed

    :param require_colons:
        whether this emoji must be wrapped in colons

    :param roles:
        roles allowed to use this emoji

    :param user:
        user that created this emoji
    """

    id: Optional[Snowflake]
    name: Optional[str]

    animated: types.APINullable[bool] = MISSING
    available: types.APINullable[bool] = MISSING
    managed: types.APINullable[bool] = MISSING
    require_colons: types.APINullable[bool] = MISSING
    roles: types.APINullable[List[Role]] = MISSING
    user: types.APINullable[User] = MISSING
