# SECURITY POLICY — LIBRAE IMMUNE AGENCY (LIA)

## Security Model of LIA

Because LIA is an immune system and enforcement layer, LIA itself is a high-value target for adversaries.

The security of LIA is guaranteed by the following core architecture requirements:
1. **Least Privilege:** LIA daemons run with minimal required OS privileges.
2. **Signed Binaries & WASM Plugins:** Plugins must be cryptographically signed and loaded into isolated WASM sandboxes.
3. **Protected State & Telemetry:** Telemetry describes events without duplicating sensitive user/model data.
4. **Immutable Audit Logs:** Incident records in Immune Memory are cryptographically signed, versioned, and attributable.
5. **Fail-Safe Design:** If LIA fails, the protected AI degrades safely according to a pre-configured policy without crashing the underlying system.

## Reporting a Vulnerability

If you discover a security vulnerability in LIA:
- Do **NOT** open a public issue.
- Report directly to `security@librae.ai` with detailed steps to reproduce.
- All reports will receive an acknowledgment within 24 hours.
