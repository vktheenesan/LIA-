# CONTRIBUTING TO LIBRAE IMMUNE AGENCY (LIA)

Thank you for contributing to LIA!

## Mandatory Developer Rules

Before submitting a Pull Request, verify that your changes adhere strictly to [`AGENTS.md`](file:///Users/sssssaranam/Desktop/LIA%20-%20Cybersecurity%20future/AGENTS.md):

1. **Small Core:** Do not add non-essential features to core. Use WASM plugins.
2. **Deterministic Safety:** Safety and containment decisions must be deterministic, not LLM-driven.
3. **Validated Recovery:** Self-healing mechanisms must undergo isolation, sandbox testing, and validation before committing to production.
4. **Reproducible Tests:** Every new capability or bug fix must include an automated test in `tests/`.
5. **No Secret Telemetry:** Never log sensitive user prompts or protected system payloads in event telemetry.

## Submission Workflow

1. Fork & clone repo.
2. Create feature branch.
3. Add implementation and test cases in `tests/`.
4. Run `graphify .` to update the project knowledge graph.
5. Run unit & integration tests (`python3 -m pytest tests/`).
6. Open PR with clear description of the capability/threat addressed.
