from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.voice import SpeakingStopEvent as SpeakingStopEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def speaking_stop_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
