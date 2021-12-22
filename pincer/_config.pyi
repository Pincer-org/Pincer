from typing import Optional

class GatewayConfig:
    socket_base_url: str
    version: int
    encoding: str
    compression: Optional[str]
    @classmethod
    def uri(cls) -> str: ...
    @classmethod
    def compressed(cls) -> bool: ...
