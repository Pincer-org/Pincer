from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.guild import GuildStatusEvent as GuildStatusEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def guild_status_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
