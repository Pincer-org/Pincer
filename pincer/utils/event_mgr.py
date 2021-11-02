# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from asyncio import (
    Event, wait_for as _wait_for, TimeoutError as _TimeoutError,
    get_running_loop
)
from typing import Any, Callable, Union

from ..exceptions import TimeoutError, AsyncGeneratorTimeoutError


class _DiscordEvent(Event):
    """
    Attributes
    ----------
    return_value : Optional[str]
        Used to store the arguments from ``can_be_set`` so they can be
        returned later.
    """

    def __init__(
        self,
        event_name: str,
        check: Union[Callable[[Any], bool], None]
    ):
        """
        Parameters
        ----------
        event_name : str
            The name of the event.
        check : Optional[Callable[[Any], bool]]
            ``can_be_set`` only returns true if this function returns true.
            Will be ignored if set to None.
        """
        self.event_name = event_name
        self.check = check
        self.return_value = None
        super().__init__()

    def can_be_set(self, event_name: str, *args) -> bool:
        """
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
        if self.event_name != event_name:
            return False

        self.return_value = args

        if self.check:
            return self.check(*args)

        return True


class EventMgr:
    """
    Attributes
    ----------
    stack : List[_DiscordEvent]
        The List of events that need to be processed.
    """

    def __init__(self):
        self.stack = []

    def add_event(self, event_name: str, check: Union[Callable, None]):
        """
        Parameters
        ----------
        event_name : str
            The type of event to listen for. Uses the same naming scheme as
            @Client.event.
        check : Optional[Callable[[Any], bool]]
            Expression to evaluate when checking if an event is valid. Will
            return be set if this event is true. Will be ignored if set to
            None.

        Returns
        -------
        _DiscordEvent
            Event that was added to the stack.
        """
        event = _DiscordEvent(
            event_name=event_name,
            check=check
        )
        self.stack.append(event)
        return event

    def pop_event(self, event) -> Any:
        """
        Parameters
        ----------
        event : _DiscordEvent
            Event to remove from the stack.

        Returns
        -------
        Any
            ``event.return_value``
        """
        self.stack.remove(event)
        return event.return_value

    def process_events(self, event_name, *args):
        """
        Parameters
        ----------
        event_name : str
            The name of the event to be processed.
        *args : Any
            The arguments returned from the middleware for this event.
        """
        for event in self.stack:
            if event.can_be_set(event_name, *args):
                event.set()

    async def wait_for(
        self,
        event_name: str,
        check: Union[Callable[[Any], bool], None],
        timeout: Union[float, None]
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
        event = self.add_event(event_name, check)
        try:
            await _wait_for(event.wait(), timeout=timeout)
        except _TimeoutError:
            raise TimeoutError(
                "wait_for() timed out while waiting for an event."
            )
        return self.pop_event(event)

    async def loop_for(
        self,
        event_name: str,
        check: Union[Callable[[Any], bool], None],
        iteration_timeout: Union[float, None],
        loop_timeout: Union[float, None],
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

        if not loop_timeout:
            while True:
                yield await self.wait_for(event_name, check, iteration_timeout)

        while True:
            start_time = get_running_loop().time()

            try:
                yield await _wait_for(
                    self.wait_for(
                        event_name,
                        check,
                        iteration_timeout
                    ),
                    timeout=loop_timeout
                )

            except _TimeoutError:
                raise AsyncGeneratorTimeoutError(
                    "loop_for() timed out while waiting for an event"
                )

            loop_timeout -= get_running_loop().time() - start_time

            # loop_timeout can be below 0 if the user's code in the for loop
            # takes longer than the time left in loop_timeout
            if loop_timeout <= 0:
                break
