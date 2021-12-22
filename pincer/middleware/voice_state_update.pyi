from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.user.voice_state import VoiceState as VoiceState
from ..utils import construct_client_dict as construct_client_dict
from typing import List, Tuple

async def voice_state_update_middleware(self, payload: GatewayDispatch) -> Tuple[str, List[VoiceState]]: ...
def export(): ...
