from typing import Any

class SlidingWindow:
    capacity: Any
    time_unit: Any
    def __init__(self, capacity: int, time_unit: float) -> None: ...
    def allow(self) -> bool: ...
