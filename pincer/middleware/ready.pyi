from ..commands import ChatCommandHandler as ChatCommandHandler
from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..exceptions import InvalidPayload as InvalidPayload
from ..objects.user.user import User as User
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro
from typing import Tuple

async def on_ready_middleware(self, payload: GatewayDispatch) -> Tuple[str]: ...
def export() -> Coro: ...
