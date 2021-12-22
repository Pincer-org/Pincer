from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.guild import GuildMemberUpdateEvent as GuildMemberUpdateEvent
from ..utils import Coro as Coro
from ..utils.conversion import construct_client_dict as construct_client_dict

async def guild_member_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
