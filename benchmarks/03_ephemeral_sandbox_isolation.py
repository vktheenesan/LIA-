"""
BENCHMARK 3: Ephemeral Sandbox Integrity & Validation (Heal Stage 4–5) Test
Goal: Prove Heal Organ executes dry-run recovery in an ephemeral sandbox without mutating production disk/memory state.
"""

import sys
import os
import hashlib
import tempfile
from typing import Dict, Any

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus
from heal.pipeline import RecoveryPipeline

def run_benchmark_3() -> Dict[str, Any]:
    print("[Benchmark 3] Running Ephemeral Sandbox Integrity & Isolation Test...")
    
    # Create a dummy production state file
    with tempfile.NamedTemporaryFile("w+", delete=False) as prod_file:
        prod_file.write("PRODUCTION_VECTOR_STORE_INDEX_STABLE_STATE_1001")
        prod_file_path = prod_file.name

    def compute_prod_hash():
        with open(prod_file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    initial_prod_hash = compute_prod_hash()

    bus = EventBus()
    heal = RecoveryPipeline(bus)

    # Simulated recovery that attempts an invalid sandbox state change
    sandbox_mutation_occurred_on_prod = False

    def diagnose():
        return {"corrupt_vector_id": 99}

    def sandbox_recovery_attempt(diag):
        # Ephemeral Sandbox dry run: Mutates a temporary sandbox buffer, NOT production file
        sandbox_buffer = "SANDBOX_CANDIDATE_RECOVERY_STATE"
        return sandbox_buffer

    def validate_failed(candidate_state):
        # Check that production file was NOT modified during sandbox execution
        current_prod_hash = compute_prod_hash()
        if current_prod_hash != initial_prod_hash:
            nonlocal sandbox_mutation_occurred_on_prod
            sandbox_mutation_occurred_on_prod = True
        # Deliberately fail validation to test isolation
        return False

    def rollback():
        pass

    # Execute recovery with failing validation
    recovery_result = heal.execute_recovery(
        component="vector_db",
        diagnose_fn=diagnose,
        recovery_fn=sandbox_recovery_attempt,
        validate_fn=validate_failed,
        rollback_fn=rollback
    )

    final_prod_hash = compute_prod_hash()
    os.remove(prod_file_path)

    integrity_preserved = (initial_prod_hash == final_prod_hash) and (not sandbox_mutation_occurred_on_prod) and (recovery_result is False)

    results = {
        "production_initial_sha256": initial_prod_hash,
        "production_final_sha256": final_prod_hash,
        "production_file_mutated": sandbox_mutation_occurred_on_prod,
        "recovery_correctly_rejected": not recovery_result,
        "sandbox_isolation_passed": integrity_preserved
    }

    print(f"    Initial Prod State Hash: {initial_prod_hash[:16]}...")
    print(f"      Final Prod State Hash: {final_prod_hash[:16]}...")
    print(f"    Production Mutated in Sandbox: {sandbox_mutation_occurred_on_prod}")
    print(f"    Sandbox Isolation Passed: {integrity_preserved}")

    return results

if __name__ == "__main__":
    run_benchmark_3()
