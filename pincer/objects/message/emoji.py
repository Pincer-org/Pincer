# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject
from ...utils.types import MISSING

if TYPE_CHECKING:
    from typing import Optional, List

    from ..user.user import User
    from ..guild.role import Role
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake


@dataclass
class Emoji(APIObject):
    """Representation of an emoji in a class.

    Attributes
    ----------
    id: Optional[:class:`~pincer.utils.snowflake.Snowflake`]
        Emoji id
    name: Optional[:class:`str`]
        Emoji name
    animated: APINullable[:class:`bool`]
        Whether this emoji is animated
    available: APINullable[:class:`bool`]
        Whether this emoji can be used, may be false due to loss of Server
        Boosts
    managed: APINullable[:class:`bool`]
        Whether this emoji is managed
    require_colons: APINullable[:class:`bool`]
        Whether this emoji must be wrapped in colons
    roles: APINullable[List[:class:`~pincer.objects.guild.role.Role`]]
        Roles allowed to use this emoji
    user: APINullable[:class:`~pincer.objects.user.user.User`]
        User that created this emoji
    """

    name: Optional[str]
    id: APINullable[Snowflake] = MISSING

    animated: APINullable[bool] = MISSING
    available: APINullable[bool] = MISSING
    managed: APINullable[bool] = MISSING
    require_colons: APINullable[bool] = MISSING
    roles: APINullable[List[Role]] = MISSING
    user: APINullable[User] = MISSING
