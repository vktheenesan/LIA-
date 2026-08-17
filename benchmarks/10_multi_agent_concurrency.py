"""
BENCHMARK 10: Multi-Agent Concurrency & Event Bus Stress Test
Goal: Prove Event Bus handles concurrent tool calls from 100 simultaneous agents without race conditions or deadlocks.
"""

import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus, NormalizedEvent

def run_benchmark_10(num_agents: int = 100, events_per_agent: int = 1000) -> Dict[str, Any]:
    total_expected_events = num_agents * events_per_agent
    print(f"[Benchmark 10] Running Multi-Agent Concurrency Stress Test ({num_agents} agents, {total_expected_events:,} total events)...")

    bus = EventBus()
    received_events: List[NormalizedEvent] = []
    lock = threading.Lock()

    def collector(event: NormalizedEvent):
        with lock:
            received_events.append(event)

    bus.subscribe_all(collector)

    def agent_worker(agent_id: int):
        for i in range(events_per_agent):
            event = NormalizedEvent(
                event_type="CONCURRENT_AGENT_TOOL_CALL",
                source=f"agent_worker_{agent_id}",
                component="shared_bus",
                metadata={"sequence": i, "agent_id": agent_id}
            )
            bus.publish(event)

    t_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=num_agents) as executor:
        futures = [executor.submit(agent_worker, a) for a in range(num_agents)]
        for f in futures:
            f.result()

    t_end = time.perf_counter()
    elapsed = t_end - t_start

    total_received = len(received_events)
    events_per_sec = total_received / elapsed if elapsed > 0 else 0

    dropped_events = total_expected_events - total_received

    results = {
        "concurrent_agents": num_agents,
        "events_per_agent": events_per_agent,
        "total_expected_events": total_expected_events,
        "total_received_events": total_received,
        "dropped_events": dropped_events,
        "elapsed_time_sec": round(elapsed, 3),
        "concurrent_throughput_eps": round(events_per_sec, 2),
        "concurrency_stress_passed": (dropped_events == 0) and (total_received == total_expected_events)
    }

    print(f"    Concurrent Agent Threads: {num_agents}")
    print(f"    Total Events Expected: {total_expected_events:,}")
    print(f"    Total Events Processed: {total_received:,}")
    print(f"    Dropped/Lost Events: {dropped_events}")
    print(f"    Concurrent Event Throughput: {results['concurrent_throughput_eps']:,} events/sec")
    print(f"    Multi-Agent Concurrency Stress Passed: {results['concurrency_stress_passed']}")

    return results

if __name__ == "__main__":
    run_benchmark_10()
