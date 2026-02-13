from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Event:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EventBus:
    def __init__(self) -> None:
        self._listeners: list[Callable[[Event], None]] = []

    def subscribe(self, listener: Callable[[Event], None]) -> Callable[[], None]:
        self._listeners.append(listener)

        def unsubscribe() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return unsubscribe

    def emit(self, event: Event) -> None:
        for listener in list(self._listeners):
            listener(event)

