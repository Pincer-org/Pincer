from ..utils.types import Coro as Coro
from typing import Dict

def get_middleware() -> Dict[str, Coro]: ...

middleware: Dict[str, Coro]
