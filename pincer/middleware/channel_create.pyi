from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..objects.guild.channel import Channel as Channel
from ..utils.conversion import construct_client_dict as construct_client_dict
from typing import Tuple

async def channel_create_middleware(self, payload: GatewayDispatch) -> Tuple[str, Channel]: ...
def export(): ...
