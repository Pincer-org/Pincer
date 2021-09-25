# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from dataclasses import dataclass, MISSING
from typing import List

from ..objects import Integration
from ..objects.user import VisibilityType
from ..utils import APIObject, APINullable


@dataclass
class Connection(APIObject):
    """
    The connection object that the user has attached.

    :param id:
        id of the connection account

    :param name:
        the username of the connection account

    :param type:
        the service of the connection (twitch, youtube)

    :param revoked:
        whether the connection is revoked

    :param integrations:
        an array of partial server integrations

    :param verified:
        whether the connection is verified

    :param friend_sync:
        whether friend sync is enabled for this connection

    :param show_activity:
        whether activities related to this connection
        will be shown in presence updates
    """
    id: str
    name: str
    type: str
    verified: bool
    friend_sync: bool
    show_activity: bool
    visibility: VisibilityType

    revoked: APINullable[bool] = MISSING
    integrations: APINullable[List[Integration]] = MISSING
