# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from asyncio import Event
from typing import Any, Callable, Optional


class _DiscordEvent(Event):

    def __init__(self, event_name: str, check: Optional[Callable[[Any], bool]]):
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
        return_value : Optional[str]
            Used to store the arguments from ``can_be_set`` so they can be
            returned later.
        """
        self.event_name = event_name
        self.check = check
        self.return_value = None
        super().__init__()

    def can_be_set(self, event_name, *args) -> bool:
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
    def __init__(self):
        """
        Attributes
        ----------
        stack : List[_DiscordEvent]
            The List of events that need to be processed.
        """
        self.stack = []

    def add_event(self, event_name: str, check: Callable):
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
            check=check,
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

    async def wait_for(self, event_name: str, check: Callable) -> Any:
        """
        Parameters
        ----------
        event_name : str
            The type of event. It should start with `on_`. This is the same
            name that is used for @Client.event.

        check : Callable[[Any], bool]
            This function only returns a value if this return true.

        Returns
        ------
        Any
            What the Discord API returns for this event.
        """
        event = self.add_event(event_name, check)
        await event.wait()
        return self.pop_event(event)

    async def loop_on(self, event_name: str, check: Callable) -> Any:
        """
        Parameters
        ----------
        event_name : str
            The type of event. It should start with `on_`. This is the same
            name that is used for @Client.event.

        check : Callable[[Any], bool]
            This function only returns a value if this return true.

        Yields
        ------
        Any
            What the Discord API returns for this event.
        """
        while True:
            yield await self.wait_for(event_name, check)
