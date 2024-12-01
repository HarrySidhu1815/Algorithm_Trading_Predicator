from abc import ABC, abstractmethod
from typing import Callable, List, Any
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
    def __init__(self, log_function: Callable[[str], None] = None):
        self._observers: List[EventObserver] = []
        self.logger = Logger(log_function)
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
    def __init__(self, log_function: Callable[[str], None]):
        
        # Initialize the logger with a custom log function.

        # param log_function: A callable function to handle log messages.

        self.log_function = log_function or self.default_log_function
    
    def default_log_function(self, message: str):
        # Default logging function (prints to terminal).
        print(message)
    
    def on_event(self, event: Any) -> None:
        # Log every incoming event.
        message = f"[Logger] Event received: {event.get('type')}"
        self.log_function(message)

    def is_interested_in(self, event: Any) -> bool:
        """Logger is interested in all events."""
        return True

