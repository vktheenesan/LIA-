"""
LIA Heal — Validated Recovery Pipeline
"""

from typing import Callable, Optional, Dict, Any
from core.event_bus import EventBus, NormalizedEvent

class RecoveryPipeline:
    """
    Safe self-healing pipeline:
    1. Detect -> 2. Isolate -> 3. Diagnose -> 4. Plan -> 5. Sandbox Test -> 6. Validate -> 7. Commit -> 8. Rollback if needed
    """

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def execute_recovery(
        self,
        component: str,
        diagnose_fn: Callable[[], Dict[str, Any]],
        recovery_fn: Callable[[Dict[str, Any]], bool],
        validate_fn: Callable[[], bool],
        rollback_fn: Callable[[], None]
    ) -> bool:
        self.event_bus.publish(NormalizedEvent(
            event_type="HEAL_STARTED",
            source="heal",
            component=component,
            severity="INFO"
        ))

        try:
            # 1. Diagnose
            diag = diagnose_fn()

            # 2. Recover in sandbox / temporary location
            success = recovery_fn(diag)
            if not success:
                raise RuntimeError("Recovery step failed during execution")

            # 3. Validate integrity
            is_valid = validate_fn()
            if not is_valid:
                raise RuntimeError("Validation failed post-recovery")

            # 4. Commit successful recovery
            self.event_bus.publish(NormalizedEvent(
                event_type="HEAL_VALIDATED",
                source="heal",
                component=component,
                severity="INFO",
                metadata={"status": "PASSED"}
            ))
            return True

        except Exception as e:
            # 5. Rollback on any failure
            rollback_fn()
            self.event_bus.publish(NormalizedEvent(
                event_type="HEAL_FAILED",
                source="heal",
                component=component,
                severity="CRITICAL",
                metadata={"error": str(e), "action": "ROLLBACK_EXECUTED"}
            ))
            return False
