from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects import StageInstance as StageInstance
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def stage_instance_delete_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
