# Librae Immune Agency (LIA) Core

> **Universal AI Immune System / Enforcement & Resilience Runtime**  
> *Small Core. Maximum Necessary Protection. Optional Capabilities.*

Librae Immune Agency (LIA) is an independent, lightweight enforcement and resilience layer designed to operate alongside AI-powered systems (Local LLMs, autonomous agents, vector databases, AI tools/plugins, servers, edge devices).

---

## 🏛️ Architecture Overview

```
             PROTECTED SYSTEM (CAHAYA / LLM / Agent)
                               │
                        observed state
                               │
                               ▼
┌────────────────────────────────────────────────────────────┐
│                    LIA CORE                                │
│                 Event / State Bus                          │
│                                                            │
│  VISION  │ Shield (Policy) │ Reflex (Containment)          │
│  HEAL (Validated Recovery) │ IMMUNE MEMORY                 │
└────────────────────────────────────────────────────────────┘
```

The core consists of **5 Essential Organs**:
1. **Vision:** Observation API across eBPF (Linux), ETW (Windows), ESF (macOS), MCP, and OpenTelemetry.
2. **Shield:** Deterministic policy checks (`ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `ISOLATE`).
3. **Reflex:** Deterministic emergency containment (block, freeze, rate-limit, isolate).
4. **Heal:** Bounded, validated recovery pipelines with mandatory sandboxing and rollbacks.
5. **Immune Memory:** Cryptographically signed, auditable incident memory.

---

## 📜 Documentation

- [Master Engineering Blueprint](file:///Users/sssssaranam/Desktop/LIA%20-%20Cybersecurity%20future/docs/01_LIA_MASTER_BLUEPRINT.md)
- [Developer Guardrails & Rules (AGENTS.md)](file:///Users/sssssaranam/Desktop/LIA%20-%20Cybersecurity%20future/AGENTS.md)
- [MVP Specification & Closed-Loop Tests](file:///Users/sssssaranam/Desktop/LIA%20-%20Cybersecurity%20future/docs/03_LIA_MVP_SPEC.md)

---

## ⚡ Quick Start

```bash
# 1. Clone repository
git clone https://github.com/librae-ai/lia.git
cd lia

# 2. Generate Graphify Knowledge Graph for AI context assistance
uv tool install graphifyy
graphify .
graphify install

# 3. Run LIA test suite
python3 -m pytest tests/
```

---

## 🛡️ License & Security

- Security policy & vulnerability reporting: see [`SECURITY.md`](file:///Users/sssssaranam/Desktop/LIA%20-%20Cybersecurity%20future/SECURITY.md).
- Contribution guidelines: see [`CONTRIBUTING.md`](file:///Users/sssssaranam/Desktop/LIA%20-%20Cybersecurity%20future/CONTRIBUTING.md).
- Licensed under the Apache-2.0 License.
