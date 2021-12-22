from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.user import VoiceState as VoiceState
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def voice_state_delete_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
