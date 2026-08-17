"""
BENCHMARK 1: High-Precision Interdiction Latency Distribution Test
Goal: Measure Shield Engine interdiction latency percentiles (P50, P90, P99, P99.9) using raw nanosecond timers.
"""

import sys
import os
import time
import csv
import statistics
from typing import Dict, Any, List

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus
from shield.engine import ShieldEngine

def run_benchmark_1(iterations: int = 100000) -> Dict[str, Any]:
    print(f"[Benchmark 1] Running High-Precision Interdiction Latency Test ({iterations:,} iterations)...")
    bus = EventBus()
    shield = ShieldEngine(bus)
    
    # Configure prohibited and allowed tools
    shield.add_prohibited_tool("rm_rf_filesystem")
    shield.add_prohibited_tool("unauthorized_exfiltration")
    
    raw_latencies_ns: List[int] = []
    csv_file = os.path.join(project_root, "benchmarks", "data", "raw_latency_ns.csv")
    
    # Pre-warm CPU cache
    for _ in range(1000):
        shield.evaluate_tool_call("agent_0", "allowed_tool")

    # High-resolution benchmark loop
    for i in range(iterations):
        tool_name = "rm_rf_filesystem" if (i % 2 == 0) else "query_knowledge_base"
        
        start_ns = time.perf_counter_ns()
        shield.evaluate_tool_call("agent_1", tool_name)
        end_ns = time.perf_counter_ns()
        
        raw_latencies_ns.append(end_ns - start_ns)

    # Save raw nanosecond data to CSV for zero-trust verification
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "latency_ns"])
        for idx, lat in enumerate(raw_latencies_ns):
            writer.writerow([idx, lat])

    sorted_lat = sorted(raw_latencies_ns)
    n = len(sorted_lat)
    
    p50_ns = sorted_lat[int(n * 0.50)]
    p90_ns = sorted_lat[int(n * 0.90)]
    p99_ns = sorted_lat[int(n * 0.99)]
    p99_9_ns = sorted_lat[int(n * 0.999)]
    mean_ns = statistics.mean(raw_latencies_ns)
    min_ns = min(raw_latencies_ns)
    max_ns = max(raw_latencies_ns)

    results = {
        "iterations": iterations,
        "mean_latency_us": round(mean_ns / 1000.0, 4),
        "min_latency_us": round(min_ns / 1000.0, 4),
        "p50_latency_us": round(p50_ns / 1000.0, 4),
        "p90_latency_us": round(p90_ns / 1000.0, 4),
        "p99_latency_us": round(p99_ns / 1000.0, 4),
        "p99_9_latency_us": round(p99_9_ns / 1000.0, 4),
        "max_latency_us": round(max_ns / 1000.0, 4),
        "raw_csv_export": csv_file
    }

    print(f"    P50 Latency: {results['p50_latency_us']} µs")
    print(f"    P90 Latency: {results['p90_latency_us']} µs")
    print(f"    P99 Latency: {results['p99_latency_us']} µs")
    print(f"  P99.9 Latency: {results['p99_9_latency_us']} µs")
    print(f"   Raw CSV exported to: {csv_file}")
    
    return results

if __name__ == "__main__":
    run_benchmark_1()
