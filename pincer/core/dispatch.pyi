from typing import Any, Dict, Optional, Union

class GatewayDispatch:
    op: Any
    data: Any
    seq: Any
    event_name: Any
    def __init__(self, op: int, data: Optional[Union[int, Dict[str, Any]]], seq: Optional[int] = ..., name: Optional[str] = ...) -> None: ...
    @classmethod
    def from_string(cls, payload: str) -> GatewayDispatch: ...
