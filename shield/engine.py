"""
LIA Shield — Deterministic Policy Engine
"""

from enum import Enum
from typing import Dict, Any, List
from core.event_bus import EventBus, NormalizedEvent

class PolicyDecision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    ISOLATE = "ISOLATE"
    LOG_ONLY = "LOG_ONLY"

class ShieldEngine:
    """
    Deterministic rule-based Policy Engine.
    Evaluates system requests, tool calls, and model requests against configured rules.
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.prohibited_tools: set = set()
        self.rules: List[Dict[str, Any]] = []

    def add_prohibited_tool(self, tool_name: str):
        self.prohibited_tools.add(tool_name)

    def evaluate_tool_call(self, agent_id: str, tool_name: str, args: Dict[str, Any] = None) -> PolicyDecision:
        if tool_name in self.prohibited_tools:
            self.event_bus.publish(NormalizedEvent(
                event_type="POLICY_VIOLATION",
                source="shield",
                component="tool_policy",
                severity="HIGH",
                metadata={"agent_id": agent_id, "tool_name": tool_name, "decision": "DENY"}
            ))
            return PolicyDecision.DENY

        return PolicyDecision.ALLOW
