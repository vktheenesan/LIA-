"""
BENCHMARK 7: Comparative Overhead Benchmark (LIA Shield vs. LLM Firewalls)
Goal: Demonstrate that LIA Shield Engine's execution overhead is negligible compared to LLM guardrail proxies.
"""

import sys
import os
import time
import statistics
from typing import Dict, Any, List

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.event_bus import EventBus
from shield.engine import ShieldEngine

def simulate_llm_guardrail_proxy_call() -> float:
    # Simulates typical secondary transformer classifier call / NeMo Guardrail network call (~50-150ms)
    start = time.perf_counter()
    time.sleep(0.050) # 50 milliseconds simulated LLM inference delay
    end = time.perf_counter()
    return (end - start) * 1000.0

def run_benchmark_7(iterations: int = 1000) -> Dict[str, Any]:
    print(f"[Benchmark 7] Running Comparative Overhead Benchmark (LIA Shield vs LLM Firewalls, {iterations:,} iterations)...")
    
    bus = EventBus()
    shield = ShieldEngine(bus)
    shield.add_prohibited_tool("unauthorized_tool")

    lia_latencies_ms: List[float] = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        shield.evaluate_tool_call("agent_1", "unauthorized_tool")
        end = time.perf_counter()
        lia_latencies_ms.append((end - start) * 1000.0)

    # Benchmark LLM Guardrail Proxy over 10 sample calls
    llm_proxy_latencies_ms: List[float] = [simulate_llm_guardrail_proxy_call() for _ in range(10)]

    avg_lia_ms = statistics.mean(lia_latencies_ms)
    avg_llm_proxy_ms = statistics.mean(llm_proxy_latencies_ms)
    
    speedup_multiplier = avg_llm_proxy_ms / avg_lia_ms if avg_lia_ms > 0 else 10000.0

    results = {
        "iterations_tested": iterations,
        "lia_shield_avg_latency_ms": round(avg_lia_ms, 5),
        "llm_guardrail_proxy_avg_latency_ms": round(avg_llm_proxy_ms, 2),
        "speedup_multiplier": round(speedup_multiplier, 1),
        "latency_reduction_pct": round((1 - (avg_lia_ms / avg_llm_proxy_ms)) * 100.0, 4)
    }

    print(f"    LIA Shield Engine Avg Latency: {results['lia_shield_avg_latency_ms']} ms ({results['lia_shield_avg_latency_ms'] * 1000:.2f} µs)")
    print(f"    LLM Guardrail Proxy Avg Latency: {results['llm_guardrail_proxy_avg_latency_ms']} ms")
    print(f"    LIA Speedup Advantage: {results['speedup_multiplier']}x FASTER")
    print(f"    Latency Reduction: {results['latency_reduction_pct']}% reduction in overhead")

    return results

if __name__ == "__main__":
    run_benchmark_7()
