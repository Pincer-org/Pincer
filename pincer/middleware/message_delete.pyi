from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.events.message import MessageDeleteEvent as MessageDeleteEvent
from ..utils.conversion import construct_client_dict as construct_client_dict
from typing import Tuple

async def on_message_delete_middleware(self, payload: GatewayDispatch) -> Tuple[str, MessageDeleteEvent]: ...
def export(): ...
