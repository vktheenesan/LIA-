#!/usr/bin/env python3
import sys
import os

# Ensure project root is in sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    print("==================================================")
    print("  LIA Core — Unit & Integration Test Runner")
    print("==================================================")

    from tests.unit.test_event_bus import test_event_bus_publish_subscribe
    from tests.unit.test_shield import test_shield_deny_prohibited_tool, test_shield_allow_permitted_tool
    from tests.integration.test_closed_loop_cahaya import test_closed_loop_cahaya_vector_recovery

    print("[1/3] Running Event Bus tests...")
    test_event_bus_publish_subscribe()
    print("      PASSED")

    print("[2/3] Running Shield Policy tests...")
    test_shield_deny_prohibited_tool()
    test_shield_allow_permitted_tool()
    print("      PASSED")

    print("[3/3] Running Closed-Loop CAHAYA Integration test...")
    test_closed_loop_cahaya_vector_recovery()
    print("      PASSED")

    print("==================================================")
    print("  ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()
