"""
LIA Vision — Observation Abstraction Layer
"""

from abc import ABC, abstractmethod
from core.event_bus import EventBus, NormalizedEvent

class BaseObserver(ABC):
    def __init__(self, event_bus: EventBus, source_name: str):
        self.event_bus = event_bus
        self.source_name = source_name
        self._is_active = False

    @abstractmethod
    def start(self):
        self._is_active = True

    @abstractmethod
    def stop(self):
        self._is_active = False

    def emit(self, event_type: str, component: str, severity: str = "INFO", metadata: dict = None):
        event = NormalizedEvent(
            event_type=event_type,
            source=self.source_name,
            component=component,
            severity=severity,
            metadata=metadata or {}
        )
        self.event_bus.publish(event)
