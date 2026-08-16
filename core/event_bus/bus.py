"""
LIA Core Event Bus — The Central Nervous System
"""

import time
import uuid
from typing import Dict, Any, Callable, List
from dataclasses import dataclass, field, asdict

@dataclass
class NormalizedEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    component: str = ""
    severity: str = "INFO"  # INFO, WARNING, HIGH, CRITICAL
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class EventBus:
    """
    Lightweight, synchronous/asynchronous Event Bus for normalized system telemetry.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[NormalizedEvent], None]]] = {}
        self._global_subscribers: List[Callable[[NormalizedEvent], None]] = []

    def subscribe(self, event_type: str, callback: Callable[[NormalizedEvent], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def subscribe_all(self, callback: Callable[[NormalizedEvent], None]):
        self._global_subscribers.append(callback)

    def publish(self, event: NormalizedEvent):
        # Notify specific event subscribers
        if event.event_type in self._subscribers:
            for callback in self._subscribers[event.event_type]:
                callback(event)

        # Notify global subscribers (e.g. Memory, Audit logs)
        for callback in self._global_subscribers:
            callback(event)
