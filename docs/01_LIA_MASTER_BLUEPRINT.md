# LIBRAE IMMUNE AGENCY (LIA) — MASTER ENGINEERING BLUEPRINT

**Company:** Librae AI Labs Sdn. Bhd.  
**Product:** Librae Immune Agency (LIA)  
**Technical Core:** LIA Core  
**Initial Protected System:** CAHAYA Sovereign AI  
**Status:** Foundational Engineering Blueprint  
**Primary Principle:** Small core. Maximum necessary protection. Optional capabilities.

---

## 1. WHAT WE ARE BUILDING

LIA is an independent, lightweight enforcement and resilience layer designed to operate alongside AI-powered systems.

The protected AI performs its intended work. LIA observes, evaluates, protects, contains, recovers, and learns. It does not replace the underlying AI.

It is capable of protecting:
- Local LLMs & Cloud-connected AI
- Autonomous agents & AI applications
- Vector databases & AI tools/plugins
- Servers, Workstations, Edge devices & Future AI runtimes

### Fundamental Architecture
```
             PROTECTED SYSTEM
       ┌───────────────────────────┐
       │ LLM / Agent / Application  │
       │ Tools / Data / OS / State  │
       └─────────────┬─────────────┘
                     │
               observed state
                     │
                     ▼
       ┌───────────────────────────┐
       │           LIA             │
       │                           │
       │ Observe                   │
       │ Analyse                   │
       │ Enforce                   │
       │ Contain                   │
       │ Heal                      │
       │ Remember                  │
       └───────────────────────────┘
```

LIA is not an AI assistant. LIA is infrastructure around intelligence.

---

## 2. THE FOUNDATIONAL RULE

**LIA Core must remain small.**

Do not turn LIA into a giant cybersecurity suite. The core provides only the mechanisms necessary to:
1. Observe
2. Establish system state
3. Detect defined abnormal conditions
4. Enforce defined policies
5. Contain defined threats
6. Recover from defined failures
7. Record what happened

Everything else is optional.

### The Litmus Test
Before adding any component, ask:
> *Can the capability be achieved without adding this component?*

If yes, prefer the simpler architecture. Target the minimum necessary complexity for reliable capability.

---

## 3. RESPONSIBILITIES OVER "AI AGENTS"

LIA does not deploy five conversational "AI people" (Tank, Scout, Guardian, Healer, Strategist). They are **responsibilities** within one protection architecture operating in parallel via events, state, telemetry, and signed records:

```
                    Event / State
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       Observe        Analyse        Policy
          │              │              │
          └──────────────┼──────────────┘
                         │
                    Enforcement
                         │
                  Recovery / Heal
                         │
                    Memory Record
```

---

## 4. THE FIVE ESSENTIAL ORGANS

1. **Vision (Observation):** Answers *"What is happening?"*
2. **Shield (Policy & Protection):** Answers *"Is this permitted?"*
3. **Reflex (Immediate Containment):** Answers *"Does something need to stop right now?"*
4. **Heal (Validated Recovery):** Answers *"Can the damaged state be safely restored?"*
5. **Immune Memory (Learning):** Answers *"What did we learn from this event?"*

---

## 5. MASTER ARCHITECTURE

```
┌────────────────────────────────────────────────────────────┐
│                  PROTECTED ORGANISM                        │
│  LLMs | Agents | Applications | Tools | Databases          │
│  Vector Stores | OS | APIs | Hardware | State              │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    LIA CORE                                │
│                 Event / State Bus                          │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ VISION                                               │  │
│  │ Linux → eBPF | Windows → ETW | macOS → ESF          │  │
│  │ Agents → MCP / OpenTelemetry                         │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │ SHIELD                                               │  │
│  │ Policy | Permission | Prompt | Data | Tool checks    │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │ REFLEX                                               │  │
│  │ Block | Freeze | Isolate | Rate-limit | Escalate     │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │ HEAL                                                 │  │
│  │ Diagnose → Recover → Validate → Commit / Rollback    │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │ IMMUNE MEMORY                                        │  │
│  │ Incident | Baseline | Recovery | Signature | Trust   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## 6. EVENT BUS — THE CENTRAL NERVOUS SYSTEM

All observers produce normalized events:
- `PROCESS_STARTED`, `FILE_CHANGED`, `NETWORK_CONNECTION`
- `TOOL_CALLED`, `MODEL_REQUEST`, `MODEL_RESPONSE`
- `POLICY_VIOLATION`, `ANOMALY_DETECTED`, `STATE_CORRUPTION`
- `HEAL_STARTED`, `HEAL_VALIDATED`, `HEAL_FAILED`, `ROLLBACK_EXECUTED`

**Critical Rule:** Telemetry describes the event; it does not unnecessarily duplicate the data being protected.

---

## 7. VISION ENGINE

Vision is an abstraction interface, not tied to a single technology:
```
                 Vision API
                     │
       ┌─────────────┼─────────────┐
       │             │             │
     Linux        Windows        macOS
      eBPF           ETW           ESF
       │             │             │
       └─────────────┼─────────────┘
                     │
               Normalized Events
```
Agent telemetry is integrated via MCP, OpenTelemetry, API interception, and application hooks.

---

## 8. SHIELD POLICY ENGINE & WASM PLUGINS

Shield enforces policy with deterministic rules: `ALLOW`, `DENY`, `REQUIRE_APPROVAL`, `ISOLATE`, `LOG_ONLY`.

Optional capabilities are provided via WebAssembly (WASM) plugins:
- `prompt-policy`, `pii-filter`, `tool-policy`, `compliance`, `custom-detector`.

---

## 9. REFLEX & SELF-HEALING

Reflex actions are strictly deterministic (e.g., Abnormal process → Freeze; Unauthorized tool → Deny; Runaway agent → Terminate). Never use an LLM for safety-critical emergency blocks.

Self-healing follows bounded, safe stages:
1. Detect → 2. Isolate → 3. Diagnose → 4. Plan → 5. Safe Sandbox Test → 6. Validate → 7. Commit → 8. Monitor → 9. Rollback if needed.

---

## 10. IMMUNE MEMORY & DOWNWARD SCALING

Incidents produce versioned, integrity-protected, auditable memory records. Fleet distribution requires cryptographic signing, provenance, and revocation to prevent immune-memory poisoning.

LIA scales downward aggressively:
- **Tiny:** Event collector + minimal policy engine + basic reflex + local state recovery.
- **Standard:** Agent observation + richer policies + anomaly detection + healing + memory.
- **Enterprise:** Fleet coordination + centralized memory + compliance + distributed telemetry.
