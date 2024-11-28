from abc import ABC, abstractmethod
from typing import List, Any
from other.singleton import make_singleton


# The EventObserver interface
class EventObserver(ABC):
    @abstractmethod
    def on_event(self, event: Any) -> None:
        """Handle an event."""
        pass

    @abstractmethod
    def is_interested_in(self, event: Any) -> bool:
        """Determine if this observer is interested in the event."""
        pass


# The EventPublisher class
@make_singleton
class EventPublisher:
    def __init__(self):
        self._observers: List[EventObserver] = []
        self.logger = Logger()
        self.subscribe(self.logger)

    def subscribe(self, observer: EventObserver) -> None:
        """Subscribe an observer to receive events."""
        self._observers.append(observer)

    def unsubscribe(self, observer: EventObserver) -> None:
        """Unsubscribe an observer from receiving events."""
        self._observers.remove(observer)

    def publish(self, event: Any) -> None:
        """Publish an event to all interested observers."""
        for observer in self._observers:
            if observer.is_interested_in(event):
                observer.on_event(event)


# Logger class that implements EventObserver
@make_singleton
class Logger(EventObserver):
    def on_event(self, event: Any) -> None:
        """Log every incoming event."""
        print(f"[Logger] Event received: {event.get('type')}")

    def is_interested_in(self, event: Any) -> bool:
        """Logger is interested in all events."""
        return True

