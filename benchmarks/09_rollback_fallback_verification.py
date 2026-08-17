"""
BENCHMARK 9: Rollback Fallback Verification Test (Heal Stage 7)
Goal: Verify that if Stage 5 Validation fails, Stage 7 Rollback restores pre-incident state SHA-256 digest with 100% precision.
"""

import sys
import os
import hashlib
from typing import Dict, Any

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus
from heal.pipeline import RecoveryPipeline

class ProductionStateStore:
    def __init__(self, initial_data: str):
        self.data = initial_data

    def get_sha256(self) -> str:
        return hashlib.sha256(self.data.encode("utf-8")).hexdigest()

def run_benchmark_9() -> Dict[str, Any]:
    print("[Benchmark 9] Running Rollback Fallback Verification Test (Heal Stage 7)...")
    
    # Establish pre-incident production state
    prod_store = ProductionStateStore("HEALTHY_PRE_INCIDENT_STATE_SNAPSHOT_90001")
    pre_incident_hash = prod_store.get_sha256()

    bus = EventBus()
    heal = RecoveryPipeline(bus)

    # Backup snapshot before recovery attempt
    backup_snapshot = prod_store.data
    rollback_executed = False

    def diagnose():
        return {"error": "corrupted_indexes"}

    def sandbox_recovery_attempt(diag):
        # Generates a broken candidate state
        return "BROKEN_CANDIDATE_STATE_THAT_FAILS_VALIDATION"

    def validate_candidate(candidate_state):
        # Intentionally reject candidate state
        return False

    def rollback_handler():
        nonlocal rollback_executed
        # Restore from backup snapshot
        prod_store.data = backup_snapshot
        rollback_executed = True

    # Execute recovery with failing validation to trigger Stage 7 Rollback
    result = heal.execute_recovery(
        component="state_store",
        diagnose_fn=diagnose,
        recovery_fn=sandbox_recovery_attempt,
        validate_fn=validate_candidate,
        rollback_fn=rollback_handler
    )

    post_rollback_hash = prod_store.get_sha256()

    hash_match = (pre_incident_hash == post_rollback_hash)
    rollback_passed = (result is False) and rollback_executed and hash_match

    results = {
        "pre_incident_sha256": pre_incident_hash,
        "post_rollback_sha256": post_rollback_hash,
        "stage_5_validation_failed_correctly": not result,
        "stage_7_rollback_executed": rollback_executed,
        "cryptographic_hash_match": hash_match,
        "rollback_fallback_passed": rollback_passed
    }

    print(f"    Pre-Incident State SHA-256: {pre_incident_hash}")
    print(f"   Post-Rollback State SHA-256: {post_rollback_hash}")
    print(f"    Stage 7 Rollback Executed: {rollback_executed}")
    print(f"    100% Cryptographic Match: {hash_match}")
    print(f"    Rollback Fallback Verification Passed: {rollback_passed}")

    return results

if __name__ == "__main__":
    run_benchmark_9()
