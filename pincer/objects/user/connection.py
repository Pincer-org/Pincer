# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass, MISSING
from typing import TYPE_CHECKING

from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import List

    from .user import VisibilityType
    from .integration import Integration
    from ...utils.types import APINullable


@dataclass
class Connection(APIObject):
    """The connection object that the user has attached.

    Attributes
    ----------
    id: :class:`str`
        Id of the connection account
    name: :class:`str`
        The username of the connection account
    type: :class:`str`
        The service of the connection (twitch, youtube)
    verified: :class:`bool`
        Whether the connection is verified
    friend_sync: :class:`bool`
        Whether friend sync is enabled for this connection
    show_activity: :class:`bool`
        Whether activities related to this connection
        will be shown in presence updates
    visibility: :class:`~pincer.objects.user.user.VisibilityType`
        If the connection is visible
    revoked: APINullable[:class:`bool`]
        Whether the connection is revoked
    integrations: APINullable[List[:class:`~pincer.objects.user.integration.Integration`]]
        An array of partial server integrations
    """
    # noqa: E501

    id: str
    name: str
    type: str
    verified: bool
    friend_sync: bool
    show_activity: bool
    visibility: VisibilityType

    revoked: APINullable[bool] = MISSING
    integrations: APINullable[List[Integration]] = MISSING
