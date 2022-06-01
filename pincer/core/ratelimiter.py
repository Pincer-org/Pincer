# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from asyncio import sleep
from dataclasses import dataclass
import logging
from time import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Tuple
    from .http import HttpCallable

_log = logging.getLogger(__name__)


@dataclass
class Bucket:
    """Represents a rate limit bucket

    Attributes
    ----------
    limit : int
        The number of requests that can be made.
    remaining : int
        The number of remaining requests that can be made.
    reset : float
        Epoch time at which rate limit resets.
    reset_after : float
        Total time in seconds until rate limit resets.
    time_cached : float
        Time since epoch when this bucket was last saved.
    """

    limit: int
    remaining: int
    reset: float
    reset_after: float
    time_cached: float


class RateLimiter:
    """Prevents ``user`` rate limits
    Attributes
    ----------
    bucket_map : Dict[Tuple[str, :class:`~pincer.core.http.HttpCallable`], str]
        Maps endpoints and methods to a rate limit bucket
    buckets : Dict[str, :class:`~pincer.core.ratelimiter.Bucket`]
        Dictionary of buckets
    """

    def __init__(self) -> None:
        self.bucket_map: Dict[Tuple[str, HttpCallable], str] = {}
        self.buckets: Dict[str, Bucket] = {}

    def save_response_bucket(
        self, endpoint: str, method: HttpCallable, header: Dict
    ):
        """
        Parameters
        ----------
        endpoint : str
            The endpoint
        method : :class:`~pincer.core.http.HttpCallable`
            The method used on the endpoint (E.g. ``Get``, ``Post``, ``Patch``)
        header : :class:`aiohttp.typedefs.CIMultiDictProxy`
            The headers from the response
        """
        bucket_id = header.get("X-RateLimit-Bucket")

        if not bucket_id:
            return

        self.bucket_map[endpoint, method] = bucket_id

        self.buckets[bucket_id] = Bucket(
            limit=int(header["X-RateLimit-Limit"]),
            remaining=int(header["X-RateLimit-Remaining"]),
            reset=float(header["X-RateLimit-Reset"]),
            reset_after=float(header["X-RateLimit-Reset-After"]),
            time_cached=time(),
        )

        _log.info(
            "Rate limit bucket detected: %s - %r.",
            bucket_id,
            self.buckets[bucket_id],
        )

    async def wait_until_not_ratelimited(
        self, endpoint: str, method: HttpCallable
    ):
        """|coro|
        Waits until the response no longer needs to be blocked to prevent a
        429 response because of ``user`` rate limits.

        Parameters
        ----------
        endpoint : str
            The endpoint
        method : :class:`~pincer.core.http.HttpCallable`
            The method used on the endpoint (E.g. ``Get``, ``Post``, ``Patch``)
        """
        bucket_id = self.bucket_map.get((endpoint, method))

        if not bucket_id:
            return

        bucket = self.buckets[bucket_id]
        cur_time = time()

        if bucket.remaining == 0:
            sleep_time = cur_time - bucket.time_cached + bucket.reset_after

            _log.info(
                "Waiting for %ss until rate limit for bucket %s is over.",
                sleep_time,
                bucket_id,
            )

            await sleep(sleep_time)

            _log.info("Message sent. Bucket %s rate limit ended.", bucket_id)
