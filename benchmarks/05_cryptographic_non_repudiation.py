"""
BENCHMARK 5: Cryptographic Audit Non-Repudiation & Tamper Test
Goal: Prove Ed25519 signatures immediately detect and reject modified historical audit logs.
"""

import sys
import os
from typing import Dict, Any, List

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus, NormalizedEvent
from memory.store import ImmuneMemoryStore

def run_benchmark_5(num_records: int = 1000) -> Dict[str, Any]:
    print(f"[Benchmark 5] Running Cryptographic Audit Non-Repudiation & Tamper Test ({num_records:,} signed records)...")
    
    bus = EventBus()
    memory = ImmuneMemoryStore(bus)

    # Generate num_records signed events
    for i in range(num_records):
        event = NormalizedEvent(
            event_type="POLICY_INTERDICTION",
            source="shield",
            component=f"agent_session_{i}",
            severity="HIGH" if i % 10 == 0 else "WARNING",
            metadata={"rule": f"rule_check_{i}"}
        )
        bus.publish(event)

    records = memory.get_records()
    total_generated = len(records)

    # Verify all records before tampering
    all_valid_before_tamper = all(memory.verify_record(r) for r in records)

    # TAMPER TEST: Intentionally flip a single bit (change 1 character) in a historical payload
    target_tamper_index = total_generated // 2
    tampered_record = dict(records[target_tamper_index])
    
    # Flip character in payload_str
    original_payload = tampered_record["payload_str"]
    tampered_payload = original_payload[:-1] + ("X" if original_payload[-1] != "X" else "Y")
    tampered_record["payload_str"] = tampered_payload

    # Run verification on tampered record
    tampered_record_valid = memory.verify_record(tampered_record)

    results = {
        "signed_records_generated": total_generated,
        "pre_tamper_all_valid": all_valid_before_tamper,
        "tampered_record_index": target_tamper_index,
        "original_payload": original_payload,
        "tampered_payload": tampered_payload,
        "tampered_record_verification_passed": tampered_record_valid,
        "tamper_detection_successful": (all_valid_before_tamper is True) and (tampered_record_valid is False)
    }

    print(f"    Generated Records: {total_generated}")
    print(f"    Pre-Tamper Verification Passed: {all_valid_before_tamper}")
    print(f"    Original Payload: '{original_payload}'")
    print(f"    Tampered Payload: '{tampered_payload}'")
    print(f"    Tampered Record Verification Result: {tampered_record_valid}")
    print(f"    Cryptographic Tamper Detection Passed: {results['tamper_detection_successful']}")

    return results

if __name__ == "__main__":
    run_benchmark_5()
