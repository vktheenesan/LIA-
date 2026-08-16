"""
LIA Reflex — Immediate Deterministic Containment
"""

from typing import Callable, Dict
from core.event_bus import EventBus, NormalizedEvent

class ReflexEngine:
    """
    Deterministic containment engine.
    Executes immediate blocks, process freezes, or isolation without LLM inference latency or risk.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe("ANOMALY_DETECTED", self.handle_anomaly)
        self.event_bus.subscribe("POLICY_VIOLATION", self.handle_policy_violation)
        self._action_handlers: Dict[str, Callable] = {}

    def register_handler(self, action_name: str, handler: Callable):
        self._action_handlers[action_name] = handler

    def handle_anomaly(self, event: NormalizedEvent):
        severity = event.severity
        if severity in ("HIGH", "CRITICAL"):
            action = "FREEZE_PROCESS" if severity == "HIGH" else "ISOLATE_COMPONENT"
            self.execute_reflex(action, event)

    def handle_policy_violation(self, event: NormalizedEvent):
        self.execute_reflex("BLOCK_ACTION", event)

    def execute_reflex(self, action: str, event: NormalizedEvent):
        if action in self._action_handlers:
            self._action_handlers[action](event)

        self.event_bus.publish(NormalizedEvent(
            event_type="REFLEX_EXECUTED",
            source="reflex",
            component=event.component,
            severity="WARNING",
            metadata={"action": action, "trigger_event_id": event.event_id}
        ))
