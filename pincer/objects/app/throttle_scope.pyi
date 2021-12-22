from enum import Enum
from typing import Any

class ThrottleScope(Enum):
    GUILD: Any
    CHANNEL: Any
    USER: Any
    GLOBAL: Any
