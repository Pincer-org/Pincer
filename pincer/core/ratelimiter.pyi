from .http import HttpCallable as HttpCallable
from typing import Any, Dict

class Bucket:
    limit: int
    remaining: int
    reset: float
    reset_after: float
    time_cached: float

class RateLimiter:
    bucket_map: Any
    buckets: Any
    def __init__(self) -> None: ...
    def save_response_bucket(self, endpoint: str, method: HttpCallable, header: Dict): ...
    async def wait_until_not_ratelimited(self, endpoint: str, method: HttpCallable): ...
