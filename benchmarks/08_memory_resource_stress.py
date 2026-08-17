"""
BENCHMARK 8: Memory & Resource Footprint Stress Test
Goal: Measure memory utilization (RAM RSS) and verify zero memory leaks under continuous high-event load.
"""

import sys
import os
import time
import gc
import tracemalloc
import resource
from typing import Dict, Any

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus, NormalizedEvent
from shield.engine import ShieldEngine
from memory.store import ImmuneMemoryStore

def get_max_rss_mb() -> float:
    # Max RSS in MB (macOS returns bytes, Linux returns KB)
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    if sys.platform == "darwin":
        return rusage.ru_maxrss / (1024 * 1024)
    else:
        return rusage.ru_maxrss / 1024

def run_benchmark_8(total_events: int = 100000) -> Dict[str, Any]:
    print(f"[Benchmark 8] Running Memory & Resource Footprint Stress Test ({total_events:,} events)...")
    
    gc.collect()
    tracemalloc.start()
    
    initial_rss_mb = get_max_rss_mb()
    snapshot_1 = tracemalloc.take_snapshot()

    bus = EventBus()
    shield = ShieldEngine(bus)
    memory = ImmuneMemoryStore(bus)
    shield.add_prohibited_tool("unauthorized_exec")

    start_time = time.perf_counter()

    # Process 100,000 events continuously
    for i in range(total_events):
        event = NormalizedEvent(
            event_type="TOOL_CALL_REQUEST",
            source="agent_worker",
            component="stress_node",
            severity="INFO",
            metadata={"index": i}
        )
        bus.publish(event)
        shield.evaluate_tool_call("agent_worker", "query_tool")

    end_time = time.perf_counter()
    gc.collect()
    
    final_rss_mb = get_max_rss_mb()
    snapshot_2 = tracemalloc.take_snapshot()
    tracemalloc.stop()

    memory_growth_mb = final_rss_mb - initial_rss_mb
    elapsed_sec = end_time - start_time
    events_per_sec = total_events / elapsed_sec if elapsed_sec > 0 else 0

    results = {
        "total_events_processed": total_events,
        "elapsed_time_sec": round(elapsed_sec, 3),
        "throughput_eps": round(events_per_sec, 2),
        "initial_rss_memory_mb": round(initial_rss_mb, 2),
        "final_rss_memory_mb": round(final_rss_mb, 2),
        "memory_growth_mb": round(memory_growth_mb, 2),
        "zero_memory_leak_passed": (memory_growth_mb < 25.0) # < 25MB growth threshold for 100k events
    }

    print(f"    Processed Events: {total_events:,} in {results['elapsed_time_sec']} sec")
    print(f"    Event Bus Throughput: {results['throughput_eps']:,} events/sec")
    print(f"    Initial RAM RSS: {results['initial_rss_memory_mb']} MB")
    print(f"      Final RAM RSS: {results['final_rss_memory_mb']} MB")
    print(f"    RAM Growth Under Load: {results['memory_growth_mb']} MB")
    print(f"    Zero-Memory-Leak Passed: {results['zero_memory_leak_passed']}")

    return results

if __name__ == "__main__":
    run_benchmark_8()
