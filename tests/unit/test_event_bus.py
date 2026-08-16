"""
Unit tests for LIA Core Event Bus
"""

from core.event_bus import EventBus, NormalizedEvent

def test_event_bus_publish_subscribe():
    bus = EventBus()
    received = []

    def on_event(event: NormalizedEvent):
        received.append(event)

    bus.subscribe("PROCESS_STARTED", on_event)

    event = NormalizedEvent(event_type="PROCESS_STARTED", source="test", component="proc")
    bus.publish(event)

    assert len(received) == 1
    assert received[0].event_type == "PROCESS_STARTED"
    assert received[0].source == "test"
