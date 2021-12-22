from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.user import User as User
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def user_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
