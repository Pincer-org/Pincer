# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import asyncio
import logging
from asyncio import TimerHandle, iscoroutinefunction
from datetime import timedelta
from typing import TYPE_CHECKING, Optional

from . import __package__
from .insertion import should_pass_cls
from ..exceptions import (
    TaskAlreadyRunning, TaskCancelError, TaskInvalidDelay,
    TaskIsNotCoroutine
)

if TYPE_CHECKING:
    from typing import Callable, Set
    from .types import Coro


_log = logging.getLogger(__package__)


class TaskScheduler:
    def __init__(self, client):
        """
        Used to create tasks
        """
        self.client = client
        self.tasks: Set[Task] = set()
        self._loop = asyncio.get_event_loop()

    def loop(
        self,
        days=0,
        weeks=0,
        hours=0,
        minutes=0,
        seconds=0,
        milliseconds=0,
        microseconds=0
    ) -> Callable[[Coro], Task]:
        """A decorator to create a task that repeat the given amount of t
        :Example usage:

        .. code-block:: python
            from pincer import Client
            from pincer.utils import TaskScheduler

            client = Client("token")
            task = TaskScheduler(client)

            @task.loop(minutes=3)
            async def my_task(self):
                ...

            my_task.start()
            client.run()

        Parameters
        ----------
        days : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        weeks : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        hours : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        minutes : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        seconds : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        milliseconds : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        microseconds : :class:`int`
            Days to wait between iterations.
            |default| ``0``
        Raises
        ------
        TaskIsNotCoroutine:
            The task is not a coroutine.
        TaskInvalidDelay:
            The delay is 0 or negative.
        """
        def decorator(func: Coro) -> Task:
            if not iscoroutinefunction(func):
                raise TaskIsNotCoroutine(
                    f'Task `{func.__name__}` is not a coroutine, '
                    'which is required for tasks.'
                )

            delay = timedelta(
                days=days,
                weeks=weeks,
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                microseconds=microseconds,
                milliseconds=milliseconds
            ).total_seconds()

            if delay <= 0:
                raise TaskInvalidDelay(
                    f'Task `{func.__name__}` has a delay of {delay} seconds, '
                    'which is invalid. Delay must be greater than zero.'
                )

            return Task(self, func, delay)

        return decorator

    def register(self, task: Task):
        """Register a task.
        Parameters
        ----------
        task : :class:`~pincer.utils.tasks.Task`
            The task to register.
        """
        self.tasks.add(task)
        self.__execute(task)

    def __execute(self, task: Task):
        """Execute a task."""
        coro = task.coro(self.client) if task.client_required else task.coro()
        # Execute the coroutine
        asyncio.ensure_future(coro)

        # Schedule the coroutine's next execution
        task._handle = self._loop.call_later(task.delay, self.__execute, task)

    def close(self):
        """Gracefully stops any running task."""
        for task in self.tasks.copy():
            if task.running:
                task.cancel()


class Task:
    """A Task is a coroutine that is scheduled to repeat every x seconds.
    Use a TaskScheduler in order to create a task.
    Parameters
    ----------
    scheduler: :class:`~pincer.utils.tasks.TaskScheduler`
        The scheduler to use.
    coro: :class:`~pincer.utils.types.Coro`
        The coroutine to register as a task.
    delay: :class:`float`
        Delay between each iteration of the task.
    """

    def __init__(self, scheduler: TaskScheduler, coro: Coro, delay: float):
        self._scheduler = scheduler
        self.coro = coro
        self.delay = delay
        self._handle: Optional[TimerHandle] = None
        self._client_required = should_pass_cls(coro)

    def __del__(self):
        if self.running:
            self.cancel()
        else:
            # Did the user forgot to call task.start() ?
            _log.warning(
                "Task `%s` was not scheduled. Did you forget to start it ?",
                self.coro.__name__
            )

    @property
    def cancelled(self):
        """:class:`bool`: Check if the task has been cancelled or not."""
        return self.running and self._handle.cancelled()

    @property
    def running(self):
        """:class:`bool`: Check if the task is running."""
        return self._handle is not None

    def start(self):
        """Register the task in the TaskScheduler and start
        the execution of the task.
        """
        if self.running:
            raise TaskAlreadyRunning(
                f'Task `{self.coro.__name__}` is already running.', self
            )

        self._scheduler.register(self)

    def cancel(self):
        """Cancel the task."""
        if not self.running:
            raise TaskCancelError(
                f'Task `{self.coro.__name__}` is not running.', self
            )

        self._handle.cancel()
        if self in self._scheduler.tasks:
            self._scheduler.tasks.remove(self)

    @property
    def client_required(self):
        return self._client_required
