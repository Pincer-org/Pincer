from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.activity import ActivityJoinEvent as ActivityJoinEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def activity_join_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
