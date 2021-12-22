from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects import UserMessage as UserMessage
from ..utils.conversion import construct_client_dict as construct_client_dict
from typing import Tuple

async def message_update_middleware(self, payload: GatewayDispatch) -> Tuple[str, UserMessage]: ...
def export(): ...
