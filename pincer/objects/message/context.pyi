from ...client import Client as Client
from ...utils.convert_message import MessageConvertable as MessageConvertable
from ...utils.snowflake import Snowflake as Snowflake
from ..app import ClientCommandStructure as ClientCommandStructure, Interaction as Interaction
from ..app.interaction_flags import InteractionFlags as InteractionFlags
from ..guild.member import GuildMember as GuildMember
from ..user.user import User as User
from .user_message import UserMessage as UserMessage
from typing import Optional, Union

class MessageContext:
    author: Union[GuildMember, User]
    command: ClientCommandStructure
    interaction: Interaction
    guild_id: Optional[Snowflake]
    channel_id: Optional[Snowflake]
    @property
    def channel(self): ...
    @property
    def guild(self): ...
    async def ack(self, flags: InteractionFlags = ...): ...
    async def reply(self, message: MessageConvertable): ...
    async def followup(self, message: MessageConvertable) -> UserMessage: ...
    async def send(self, message: MessageConvertable) -> UserMessage: ...
