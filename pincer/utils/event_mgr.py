# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import Event, wait_for as _wait_for, get_running_loop, TimeoutError
from collections import deque
from typing import TYPE_CHECKING

from ..exceptions import TimeoutError as PincerTimeoutError

if TYPE_CHECKING:
    from typing import Any, List, Union, Optional
    from .types import CheckFunction


class _Processable(ABC):

    @abstractmethod
    def process(self, event_name: str, *args):
        """
        Method that is ran when an event is received from discord.

        Parameters
        ----------
        event_name : str
            The name of the event.
        *args : Any
            Arguments to evaluate check with.

        Returns
        -------
        bool
            Whether the event can be set
        """

    def matches_event(self, event_name: str, *args):
        """
        Parameters
        ----------
        event_name : str
            Name of event.
        *args : Any
            Arguments to eval check with.
        """
        if self.event_name != event_name:
            return False

        if self.check:
            return self.check(*args)

        return True


def _lowest_value(*args):
    """
    Returns lowest value from list of numbers. ``None`` is not counted as a
    value. ``None`` is returned if all arguments are ``None``.
    """
    args_without_none = [n for n in args if n is not None]

    if not args_without_none:
        return None

    return min(args_without_none)


class _Event(_Processable):
    """
    Parameters
    ----------
    event_name : str
        The name of the event.
    check : Optional[Callable[[Any], bool]]
        ``can_be_set`` only returns true if this function returns true.
        Will be ignored if set to None.

    Attributes
    ----------
    event : :class:`asyncio.Event`
        Even that is used to wait until the next valid discord event.
    return_value : Optional[str]
        Used to store the arguments from ``can_be_set`` so they can be
        returned later.
    """

    def __init__(
        self,
        event_name: str,
        check: CheckFunction
    ):
        self.event_name = event_name
        self.check = check
        self.event = Event()
        self.return_value = None
        super().__init__()

    async def wait(self):
        """
        Waits until ``self.event`` is set.
        """
        await self.event.wait()

    def process(self, event_name: str, *args) -> bool:
        if self.matches_event(event_name, *args):
            self.return_value = args
            self.event.set()


class _LoopEmptyError(Exception):
    """Raised when the _LoopMgr is empty and cannot accept new item"""


class _LoopMgr(_Processable):
    """
    Parameters
    ----------
    event_name : str
        The name of the event.
    check : Optional[Callable[[Any], bool]]
        ``can_be_set`` only returns true if this function returns true.
        Will be ignored if set to None.

    Attributes
    ----------
    can_expand : bool
        Whether the queue is allowed to grow. Turned to false once the
        EventMgr's timer runs out.
    events : :class:`collections.deque`
        Queue of events to be processed.
    wait : :class:`asyncio.Event`
        Used to make ``get_next()` wait for the next event.
    """

    def __init__(self, event_name: str, check: CheckFunction) -> None:
        self.event_name = event_name
        self.check = check

        self.can_expand = True
        self.events = deque()
        self.wait = Event()

    def process(self, event_name: str, *args):
        if not self.can_expand:
            return

        if self.matches_event(event_name, *args):
            self.events.append(args)
            self.wait.set()

    async def get_next(self):
        """
        Returns the next item if the queue. If there are no items in the queue,
        it will return the next event that happens.
        """
        if not self.events:
            if not self.can_expand:
                raise _LoopEmptyError

            self.wait.clear()
            await self.wait.wait()
        return self.events.popleft()


class EventMgr:
    """
    Attributes
    ----------
    event_list : List[_DiscordEvent]
        The List of events that need to be processed.
    """

    def __init__(self):
        self.event_list: List[_Processable] = []

    def process_events(self, event_name, *args):
        """
        Parameters
        ----------
        event_name : str
            The name of the event to be processed.
        *args : Any
            The arguments returned from the middleware for this event.
        """
        for event in self.event_list:
            event.process(event_name, *args)

    async def wait_for(
        self,
        event_name: str,
        check: CheckFunction,
        timeout: Optional[float]
    ) -> Any:
        """
        Parameters
        ----------
        event_name : str
            The type of event. It should start with `on_`. This is the same
            name that is used for @Client.event.
        check : Union[Callable[[Any], bool], None]
            This function only returns a value if this return true.
        timeout: Union[float, None]
            Amount of seconds before timeout. Use None for no timeout.

        Returns
        ------
        Any
            What the Discord API returns for this event.
        """

        event = _Event(event_name, check)
        self.event_list.append(event)

        try:
            await _wait_for(event.wait(), timeout=timeout)
        except TimeoutError:
            raise PincerTimeoutError(
                "wait_for() timed out while waiting for an event."
            )
        self.event_list.remove(event)
        return event.return_value

    async def loop_for(
        self,
        event_name: str,
        check: CheckFunction,
        iteration_timeout: Optional[float],
        loop_timeout: Optional[float],
    ) -> Any:
        """
        Parameters
        ----------
        event_name : str
            The type of event. It should start with `on_`. This is the same
            name that is used for @Client.event.
        check : Callable[[Any], bool]
            This function only returns a value if this return true.
        iteration_timeout: Union[float, None]
            Amount of seconds before timeout. Timeouts are for each loop.
        loop_timeout: Union[float, None]
            Amount of seconds before the entire loop times out. The generator
            will only raise a timeout error while it is waiting for an event.

        Yields
        ------
        Any
            What the Discord API returns for this event.
        """

        loop_mgr = _LoopMgr(event_name, check)
        self.event_list.append(loop_mgr)

        loop = get_running_loop()

        while True:
            start_time = loop.time()

            try:
                yield await _wait_for(
                    loop_mgr.get_next(),
                    timeout=_lowest_value(
                        loop_timeout, iteration_timeout
                    )
                )

            except TimeoutError:
                # Loop timed out. Loop through the remaining events received
                # before the timeout.
                loop_mgr.can_expand = False
                try:
                    while True:
                        yield await loop_mgr.get_next()
                except _LoopEmptyError:
                    raise PincerTimeoutError(
                        "loop_for() timed out while waiting for an event"
                    )

            # `not` can't be used here because there is a check for
            # `loop_timeout == 0`
            if loop_timeout is not None:
                loop_timeout -= loop.time() - start_time

                # loop_timeout can be below 0 if the user's code in the for loop
                # takes longer than the time left in loop_timeout
                if loop_timeout <= 0:
                    raise PincerTimeoutError(
                        "loop_for() timed out while waiting for an event"
                    )
