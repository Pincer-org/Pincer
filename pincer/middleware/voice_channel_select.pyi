from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.voice import VoiceChannelSelectEvent as VoiceChannelSelectEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def voice_channel_select_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
