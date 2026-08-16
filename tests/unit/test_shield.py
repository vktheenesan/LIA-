"""
Unit tests for Shield Policy Engine
"""

from core.event_bus import EventBus
from shield.engine import ShieldEngine, PolicyDecision

def test_shield_deny_prohibited_tool():
    bus = EventBus()
    shield = ShieldEngine(bus)

    violations = []
    bus.subscribe("POLICY_VIOLATION", lambda e: violations.append(e))

    shield.add_prohibited_tool("rm_rf_all")

    decision = shield.evaluate_tool_call(agent_id="cahaya_agent_1", tool_name="rm_rf_all")
    assert decision == PolicyDecision.DENY
    assert len(violations) == 1
    assert violations[0].metadata["tool_name"] == "rm_rf_all"

def test_shield_allow_permitted_tool():
    bus = EventBus()
    shield = ShieldEngine(bus)

    decision = shield.evaluate_tool_call(agent_id="cahaya_agent_1", tool_name="search_db")
    assert decision == PolicyDecision.ALLOW
