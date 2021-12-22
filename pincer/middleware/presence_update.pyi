from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.presence import PresenceUpdateEvent as PresenceUpdateEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def presence_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
