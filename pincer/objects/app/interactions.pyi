from ...exceptions import InteractionAlreadyAcknowledged as InteractionAlreadyAcknowledged, InteractionDoesNotExist as InteractionDoesNotExist, InteractionTimedOut as InteractionTimedOut, NotFoundError as NotFoundError, UseFollowup as UseFollowup
from ...utils import APINullable as APINullable, APIObject as APIObject
from ...utils.convert_message import MessageConvertable as MessageConvertable, convert_message as convert_message
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import MISSING as MISSING
from ..app.select_menu import SelectOption as SelectOption
from ..guild.channel import Channel as Channel
from ..guild.member import GuildMember as GuildMember
from ..guild.role import Role as Role
from ..message.context import MessageContext as MessageContext
from ..message.message import Message as Message
from ..message.user_message import UserMessage as UserMessage
from ..user import User as User
from .command import AppCommandInteractionDataOption as AppCommandInteractionDataOption
from .command_types import AppCommandOptionType as AppCommandOptionType
from .interaction_base import CallbackType as CallbackType, InteractionType as InteractionType
from .interaction_flags import InteractionFlags as InteractionFlags
from .mentionable import Mentionable as Mentionable
from pincer.utils.api_object import ChannelProperty as ChannelProperty, GuildProperty as GuildProperty
from typing import Any, Dict, List, Optional, Union

class ResolvedData(APIObject):
    users: APINullable[Dict[Snowflake, User]]
    members: APINullable[Dict[Snowflake, GuildMember]]
    roles: APINullable[Dict[Snowflake, Role]]
    channels: APINullable[Dict[Snowflake, Channel]]
    messages: APINullable[Dict[Snowflake, UserMessage]]

class InteractionData(APIObject):
    id: Snowflake
    name: str
    type: int
    resolved: APINullable[ResolvedData]
    options: APINullable[List[AppCommandInteractionDataOption]]
    custom_id: APINullable[str]
    component_type: APINullable[int]
    values: APINullable[SelectOption]
    target_id: APINullable[Snowflake]

class Interaction(APIObject, ChannelProperty, GuildProperty):
    id: Snowflake
    application_id: Snowflake
    type: InteractionType
    token: str
    version: int
    data: APINullable[InteractionData]
    guild_id: APINullable[Snowflake]
    channel_id: APINullable[Snowflake]
    member: APINullable[GuildMember]
    user: APINullable[User]
    message: APINullable[UserMessage]
    has_replied: bool
    has_acknowledged: bool
    def __post_init__(self) -> None: ...
    @staticmethod
    def return_type(option: Snowflake, data: Dict[Snowflake, Any]) -> Optional[APIObject]: ...
    def convert_to_message_context(self, command): ...
    async def response(self) -> UserMessage: ...
    async def ack(self, flags: Optional[InteractionFlags] = ...): ...
    async def reply(self, message: MessageConvertable): ...
    async def edit(self, message: MessageConvertable) -> UserMessage: ...
    async def delete(self) -> None: ...
    async def followup(self, message: MessageConvertable) -> UserMessage: ...
    async def edit_followup(self, message_id: int, message: MessageConvertable) -> UserMessage: ...
    async def get_followup(self, message_id: int) -> UserMessage: ...
    async def delete_followup(self, message: Union[UserMessage, int]): ...
