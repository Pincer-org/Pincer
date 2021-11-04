# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.


from dataclasses import dataclass

from ...objects.message import UserMessage
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake


@dataclass
class NotificationCreateEvent(APIObject):
    """
    Represents a notification

    Attributes
    ----------
    channel_id : :class:`Snowflake`
        id of channel where notification occurred

    message : :class:`UserMessage`
        message that generated this notification

    icon_url : :class:`str`
        icon url of the notification

    title : :class:`str`
        title of the notification

    body : :class:`str`
        body of the notification
    """

    channel_id: Snowflake
    message: UserMessage
    icon_url: str
    title: str
    body: str
