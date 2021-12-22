from pincer.core import __package__ as __package__
from ..core.dispatch import GatewayDispatch as GatewayDispatch
from ..exceptions import HeartbeatError as HeartbeatError
from websockets.legacy.client import WebSocketClientProtocol as WebSocketClientProtocol

class Heartbeat:
    @classmethod
    def get(cls) -> float: ...
    @classmethod
    async def handle_hello(cls, socket: WebSocketClientProtocol, payload: GatewayDispatch): ...
    @classmethod
    async def handle_heartbeat(cls, socket: WebSocketClientProtocol, _): ...
    @classmethod
    def update_sequence(cls, seq: int): ...
