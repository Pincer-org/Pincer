from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.guild import GuildStickersUpdateEvent as GuildStickersUpdateEvent
from ..utils import Coro as Coro
from ..utils.conversion import construct_client_dict as construct_client_dict

async def guild_stickers_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
