from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.message import MessageDeleteBulkEvent as MessageDeleteBulkEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def message_delete_bulk_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
