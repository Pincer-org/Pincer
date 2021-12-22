from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.guild import GuildMemberAddEvent as GuildMemberAddEvent
from ..utils import Coro as Coro
from ..utils.conversion import construct_client_dict as construct_client_dict

async def guild_member_add_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
