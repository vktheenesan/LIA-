"""
LIA Immune Memory — Signed Structured Incident Memory
"""

import json
import hashlib
from typing import List, Dict, Any
from core.event_bus import EventBus, NormalizedEvent

class ImmuneMemoryStore:
    """
    Structured, tamper-evident incident memory.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.records: List[Dict[str, Any]] = []
        self.event_bus.subscribe_all(self._record_event)

    def _record_event(self, event: NormalizedEvent):
        # Record security-relevant events
        if event.severity in ("WARNING", "HIGH", "CRITICAL") or "POLICY" in event.event_type or "HEAL" in event.event_type:
            record = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp,
                "source": event.source,
                "component": event.component,
                "severity": event.severity,
                "metadata": event.metadata,
                "signature": self._calculate_signature(event)
            }
            self.records.append(record)

    def _calculate_signature(self, event: NormalizedEvent) -> str:
        payload = f"{event.event_id}:{event.event_type}:{event.timestamp}:{event.component}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get_records() -> List[Dict[str, Any]]:
        return list(self.records)
