# TRADE SECRET PROTECTION & PROPRIETARY EXTENSION ARCHITECTURE

**Company:** Librae AI Labs  
**Product:** Librae Immune Agency (LIA)

---

## 1. Architectural Separation Principle

To ensure LIA Core can be freely shared with the open-source community as **Patient 0** while protecting Librae AI Labs' proprietary trade secrets and enterprise IP, LIA relies on strict WASM-based plugin boundaries and interface abstraction.

```
┌─────────────────────────────────────────────────────────────┐
│                    OPEN SOURCE CORE                         │
│  LIA Core Event Bus | Policy Interface | Recovery Pipeline   │
│  Vision Abstraction | Memory Store Schema | Base Reflex     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                WASM ABI / Plugin Interface
                               │
┌──────────────────────────────▼──────────────────────────────┐
│            PROPRIETARY ENTERPRISE EXTENSIONS               │
│  Proprietary Anomaly Models | Advanced Behavioral ML         │
│  Custom Sovereign AI Adapters | Fleet Intelligence Mesh      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Core vs. Proprietary Boundaries

| Component | Open Source Core (Community) | Proprietary / Trade Secret (Librae AI) |
|---|---|---|
| **Event Bus** | Normalized JSON telemetry & bus engine | Distributed cross-node encryption mesh |
| **Shield Engine** | Deterministic rule matching engine | Advanced LLM prompt injection detectors |
| **Reflex Engine** | Deterministic block/freeze mechanisms | Automated fleet-wide response orchestration |
| **Heal Pipeline** | 8-Stage safe recovery state machine | Proprietary automated code repair models |
| **Immune Memory** | Signed JSON audit logs | Cryptographic fleet trust & consensus network |

---

## 3. Developing Proprietary Plugins Without Modifying Core

1. Write custom detectors as compiled WebAssembly (`.wasm`) binaries.
2. Place WASM plugins inside the `plugins/` directory.
3. Core loads plugins into isolated, sandboxed runtimes without exposing core source code or embedding enterprise IP into the open-source distribution.
