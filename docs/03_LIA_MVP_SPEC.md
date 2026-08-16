# LIA MVP SPECIFICATION — CLOSED-LOOP TEST 1: CAHAYA SOVEREIGN AI

**Objective:** Prove one complete closed loop on CAHAYA Sovereign AI before expanding scope.

```
       CAHAYA Sovereign AI
               │
      Failure / Attack introduced
               │
          LIA Observes
               │
          LIA Detects
               │
          LIA Contains
               │
          LIA Recovers
               │
          LIA Validates
               │
        CAHAYA Resumes
               │
       LIA Records Memory
```

---

## 1. TARGET SYSTEM: CAHAYA SOVEREIGN AI

CAHAYA deployment components:
- **AI Runtime:** Local LLM service / agent runtime
- **Agents:** Execution environment
- **Vector Stores:** Vector database / Index
- **Services:** API endpoints and background workers

LIA Core protects CAHAYA while remaining strictly decoupled.

---

## 2. FOUR INITIAL MVP DEMONSTRATION TEST CASES

### Test A — Runaway Process / Resource Anomaly
1. Agent enters infinite execution loop / excessive memory consumption.
2. **Vision** detects resource threshold violation and emits `ANOMALY_DETECTED`.
3. **Reflex** isolates/freezes process without LLM intervention.
4. Process stopped cleanly; event logged in **Immune Memory**.

### Test B — Vector State Corruption & Recovery
1. Controlled data corruption injected into vector store index.
2. **Vision** detects index integrity mismatch (`STATE_CORRUPTION`).
3. **Reflex** halts writes to vector store.
4. **Heal** identifies last known-good checkpoint, rebuilds index in temporary sandbox, runs integrity checks, swaps validated index, and resumes service.
5. **Validation** confirms 100% integrity before resuming traffic.

### Test C — Unauthorized Tool Access
1. Agent requests prohibited tool execution (e.g. unauthorized terminal command).
2. **Shield** evaluates call against policy rules.
3. Policy returns `DENY`.
4. Agent call blocked; audit record emitted (`POLICY_VIOLATION`).
5. Agent continues safe operation without crashing.

### Test D — LIA Failure & Resiliency (Fail-Safe Verification)
1. LIA daemon process is intentionally killed (`SIGKILL`).
2. **CAHAYA** continues running according to configured fail-open policy.
3. System alert generated.
4. LIA daemon restarted; monitoring and protection automatically resume.

---

## 3. ACCEPTANCE CRITERIA FOR MVP

- Zero false positives on baseline CAHAYA test run.
- All 4 test cases pass with reproducible, automated test scripts in `tests/integration/` and `tests/recovery/`.
- Average observation overhead < 2% CPU and < 50MB RAM.
- Complete audit trail created for every event in structured JSON memory format.
