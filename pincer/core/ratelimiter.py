# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from asyncio import sleep
from dataclasses import dataclass
from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict
    from .http import HttpCallable


@dataclass
class Bucket:
    limit: int
    remaining: int
    reset: float
    reset_after: float
    time_cached: float


class RateLimiter:
    def __init__(self) -> None:
        self.bucket_map: Dict[str, str] = {}
        self.buckets: Dict[str, Bucket] = {}

    def save_response_bucket(
        self,
        endpoint: str,
        method: HttpCallable,
        header: Dict
    ):

        if bucket_id := header.get("X-RateLimit-Bucket"):
            self.bucket_map[endpoint, method] = bucket_id

            self.buckets[bucket_id] = Bucket(
                limit=int(header["X-RateLimit-Limit"]),
                remaining=int(header["X-RateLimit-Remaining"]),
                reset=float(header["X-RateLimit-Reset"]),
                reset_after=float(header["X-RateLimit-Reset-After"]),
                time_cached=time()
            )

    async def wait_until_not_ratelimited(
        self,
        endpoint: str,
        method: HttpCallable
    ):
        bucket_id = self.bucket_map.get((endpoint, method), None)

        if bucket_id is None:
            return

        bucket = self.buckets[bucket_id]
        cur_time = time()

        if bucket.remaining == 0:
            await sleep(cur_time - bucket.time_cached + bucket.reset_after)
