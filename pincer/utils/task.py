# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
# TODO: Documentation

import asyncio
import warnings
from asyncio import iscoroutinefunction
from asyncio.events import TimerHandle
from datetime import timedelta
from inspect import getfullargspec
from typing import Callable, Set

from .types import Coro


class Task:
    def __init__(self, coro: Coro, delay: float, client=None):
        self.coro = coro
        self.delay = delay
        self.client = client
        self._handle: TimerHandle = None
        self._client_required = len(getfullargspec(coro).args) == 1

    def __del__(self):
        # Did the user forgot to call task.start() ?
        if self._handle is None:
            pass
            # TODO: warn user the task was not scheduled.

    @property
    def cancelled(self):
        return self.running and self._handle.cancelled()

    @property
    def running(self):
        return self._handle is not None

    def start(self, client=None):
        if self.running:
            # TODO: New exception with more debug info
            raise Exception('Task is already running')

        if client is not None:
            self.client = client

        if self.client is None and self._client_required:
            raise Exception('No client bound to the task')

        self.__execute()

    def cancel(self):
        if not self.running:
            # TODO: New exception with more debug info
            raise Exception('Task is not running')

        self._handle.cancel()

    def __execute(self):
        if self._client_required:
            coro = self.coro(self.client)
        else:
            coro = self.coro()

        # Execute the coroutine
        asyncio.ensure_future(coro)

        # Schedule the coroutine's next execution
        loop = asyncio.get_event_loop()
        self._handle = loop.call_later(self.delay, self.__execute)


class TaskScheduler:
    def __init__(self, client):
        self.client = client
        self.register: Set[Task] = set()

    def __del__(self):
        self.close()

    def loop(
        self,
        days=0,
        weeks=0,
        hours=0,
        minutes=0,
        seconds=0,
        microseconds=0,
        milliseconds=0
    ) -> Callable[[Coro], Task]:
        def decorator(func: Coro) -> Task:
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
            self.register.add(task := Task(func, delay, self.client))

            return task

        return decorator

    def close(self):
        """Gracefully stops any running task."""
        for task in self.register:
            if task.running:
                task.cancel()
