from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects import Emoji as Emoji
from ..objects.events.message import MessageReactionRemoveEvent as MessageReactionRemoveEvent
from ..utils.conversion import construct_client_dict as construct_client_dict

async def message_reaction_remove_middleware(self, payload: GatewayDispatch): ...
def export(): ...
