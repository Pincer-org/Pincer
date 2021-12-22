from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.typing_start import TypingStartEvent as TypingStartEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def typing_start_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
