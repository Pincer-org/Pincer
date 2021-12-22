from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects import StageInstance as StageInstance
from ..utils import Coro as Coro, replace as replace
from ..utils.conversion import construct_client_dict as construct_client_dict

async def stage_instance_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
