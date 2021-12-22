from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.voice_settings import VoiceSettingsUpdateEvent as VoiceSettingsUpdateEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro

async def voice_settings_update_middleware(self, payload: GatewayDispatch): ...
def export() -> Coro: ...
