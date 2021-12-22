from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.guild import GuildIntegrationsUpdateEvent as GuildIntegrationsUpdateEvent
from ..utils import Coro as Coro
from ..utils.conversion import construct_client_dict as construct_client_dict

async def guild_integrations_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
