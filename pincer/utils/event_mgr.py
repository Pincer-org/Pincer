# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from asyncio import Event
from typing import Any, Callable


class _DiscordEvent(Event):

    def __init__(self, event_name, check):
        self.event = event_name
        self.check = check
        self.return_value = None
        super().__init__()

    def can_be_set(self, event, *args) -> bool:

        if self.event != event:
            return False

        self.return_value = args

        if self.check:
            return self.check(*args)

        return True


class EventMgr:
    def __init__(self):
        self.stack = []

    def add_event(self, event_name: str, check: Callable):
        event = _DiscordEvent(
            event_name=event_name,
            check=check,
        )
        self.stack.append(event)
        return event

    def pop_event(self, event) -> _DiscordEvent:
        event = self.stack.pop(self.stack.index(event))
        return event.return_value

    def process_events(self, event_name, *args):
        for event in self.stack:
            if event.can_be_set(event_name, *args):
                event.set()

    async def wait_for(self, event_name: str, check: Callable = None) -> Any:
        event = self.add_event(event_name, check)
        await event.wait()
        return self.pop_event(event)

    async def loop_on(self, event_name: str, check: Callable = None) -> Any:
        while True:
            yield self.wait_for(event_name, check)
