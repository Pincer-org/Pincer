from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.invite import InviteDeleteEvent as InviteDeleteEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def invite_delete_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
