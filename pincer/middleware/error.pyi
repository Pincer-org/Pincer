from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.error import DiscordError as DiscordError
from ..utils.conversion import construct_client_dict as construct_client_dict
from ..utils.types import Coro as Coro
from typing import Tuple

def error_middleware(self, payload: GatewayDispatch) -> Tuple[str, DiscordError]: ...
def export() -> Coro: ...
