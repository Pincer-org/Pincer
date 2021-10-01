# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
# TODO: Documentation

import asyncio
import warnings
from asyncio import iscoroutinefunction
from asyncio.events import TimerHandle
from datetime import timedelta

from .types import Coro


def loop(
    days=0,
    weeks=0,
    hours=0,
    minutes=0,
    seconds=0,
    microseconds=0,
    milliseconds=0
):
    def decorator(func: Coro):
        if not iscoroutinefunction(func):
            # TODO: New exception with more debug info
            raise Exception('Not a coroutine.')

        delay = timedelta(
            days=days,
            weeks=weeks,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds
        ).total_seconds()

        return Task(func, delay)

    return decorator


class Task:
    def __init__(self, coro: Coro, delay: float):
        self.coro = coro
        self.delay = delay
        self._handle: TimerHandle = None

    def __del__(self):
        # Did the user forgot to call task.start() ?
        if self._handle is None:
            pass
            # TODO: warn user the task was not scheduled.

    @property
    def cancelled(self):
        return self._handle is not None and self._handle.cancelled()

    def start(self):
        if self._handle is not None:
            # TODO: New exception with more debug info
            raise Exception('Task is already running')

        self.__execute()

    def cancel(self):
        if self._handle is None:
            # TODO: New exception with more debug info
            raise Exception('Task is not running')

        self._handle.cancel()

    def __execute(self):
        # Execute the coroutine
        # TODO: give the client as argument
        asyncio.ensure_future(self.coro())

        # Schedule the coroutine's next execution
        loop = asyncio.get_event_loop()
        self._handle = loop.call_later(self.delay, self.__execute)
