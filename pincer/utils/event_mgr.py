# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from asyncio import Event
from dataclasses import dataclass
from typing import Callable


@dataclass
class _DiscordEvent(Event):
    event: str
    check: Callable = None

    def can_be_set(self, event, *args) -> bool:
        if self.event != event:
            return False

        if not self.check:
            return self.check(*args)

        return True


class EventMgr():
    def __init__(self):
        self.stack = list()

    def add_event(self, event_name: str, check: Callable = None):
        event = _DiscordEvent(
            event=event_name,
            check=check,
        )
        self.stack.append(event)
        return event

    def remove_event(self, event: _DiscordEvent):
        self.stack.remove(event)

    def process_events(self, event, *args):
        for event in self.stack:
            if event.can_be_set(event, *args):
                event.set()
                self.remove_event(event)
