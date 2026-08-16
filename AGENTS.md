# AGENTS.md — DEVELOPER & AI ASSISTANT GUARDRAILS

> **THE LIA GOLDEN RULE**  
> Build the smallest system capable of providing the required protection.  
> Observe before intervening.  
> Never make an unvalidated repair.  
> Never trust an unverified signal.  
> Every intervention must be explainable and auditable.  
> Every failure must make LIA harder to break in the same way again.  
> Keep the core lightweight. Put optional complexity in replaceable modules.  
> Protect the capability; keep the implementation replaceable.

---

## 1. TWENTY ENGINEERING RULES

1. **Rule 1** — Do not build speculative features.
2. **Rule 2** — Core stays minimal.
3. **Rule 3** — Plugins before core expansion.
4. **Rule 4** — No silent autonomous production modifications.
5. **Rule 5** — Every automatic repair must have validation.
6. **Rule 6** — Every intervention produces an audit event.
7. **Rule 7** — Every failure produces a regression test where practical.
8. **Rule 8** — Never trust an external event or memory record by default.
9. **Rule 9** — No secret or protected data in telemetry unless explicitly required.
10. **Rule 10** — No unnecessary network dependency (local-first design).
11. **Rule 11** — LIA must degrade safely when its own components fail.
12. **Rule 12** — Never use an LLM for a deterministic safety decision when a deterministic mechanism is sufficient.
13. **Rule 13** — Every dependency must justify its existence.
14. **Rule 14** — No hard-coded vendor dependency in the core.
15. **Rule 15** — Benchmark before making performance claims.
16. **Rule 16** — Security changes require adversarial testing.
17. **Rule 17** — Never claim "self-healing" until recovery has been demonstrated and validated.
18. **Rule 18** — Never claim cross-platform support until independently tested on that platform.
19. **Rule 19** — Every significant architecture decision gets documented.
20. **Rule 20** — If something breaks, ask why it was possible and convert the lesson into a permanent guardrail (The Phoenix Principle).

---

## 2. RED FLAG MITIGATION MATRIX

| Red Flag | Description | Mandatory Architectural Mitigation |
|---|---|---|
| **RED FLAG 1: Bloat** | Immune system becomes a huge, complex platform | Move non-essential features out of core into WASM plugins. |
| **RED FLAG 2: Too many AI components** | Implementing separate "AI agents" for roles | Use deterministic modules communicating over normalized event buses. |
| **RED FLAG 3: Autonomous repair damage** | AI guesses fixes and alters production | Strict stage pipeline: Isolate → Diagnose → Test in sandbox → Validate → Commit → Rollback. |
| **RED FLAG 4: False Positives** | Security interrupts normal work, gets disabled | Monitor mode first → Establish baseline → Require high confidence policy intervention. |
| **RED FLAG 5: Memory Poisoning** | One compromised node poisons fleet intelligence | Cryptographically signed, attributed, versioned, revocable memory records. |
| **RED FLAG 6: Single Point of Failure** | LIA failure crashes the protected AI | Protected system must survive LIA failure via configurable fail-open/fail-closed policy. |
| **RED FLAG 7: Vendor Lock-in** | Core depends on specific LLM, cloud, or framework | Generic adapters and clean interface abstractions. |
| **RED FLAG 8: Weak Evidence** | Impressive demo without empirical proof | Every key capability must have a reproducible automated test. |
| **RED FLAG 9: Feature Creep** | Developer builds features because they are interesting | Justify: What problem does it solve? Why does it need to exist? What happens without it? |

---

## 3. DEVELOPMENT WORKFLOW

Before writing significant code, follow this sequence:
```
Understand → Define capability → Define threat/failure → Define minimum mechanism → Design interface → Implement → Test → Attack → Measure → Document → Integrate
```

---

## 4. CONTEXT EFFICIENCY GUIDELINE

Maintain a lightweight repository dependency and architecture graph (`graphify`) so AI-assisted development retrieves only the files and symbols relevant to the active task without feeding the entire codebase into context.
