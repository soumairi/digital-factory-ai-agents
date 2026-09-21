# Test the Backend Implementation

Apply the [Backend Agent contract](../core/agent.md), all linked core documents, and shared policies. Read project test instructions and inspect actual implementation changes before selecting commands. Confirm the environment is authorized and non-production; use safe fixtures.

Run acceptance and relevant regression tests and security checks. Assess all six [negative-test categories](../core/definition-of-done.md#automated-negative-test-gate): unauthenticated access, unauthorized access, ownership boundaries, invalid inputs, malicious inputs, and sensitive field manipulation. Add or repair missing applicable automated tests within scope and run them. Verify protected state and response contents as well as status codes.

Report exact commands, environment/revision, results, evidence, failures, and skipped checks with reasons. Record justified non-applicability; inability to execute is not non-applicability. Investigate failures without weakening tests or controls, and rerun affected checks after fixes. Missing or failing required checks prevent Done. Hand off evidence for self-review without merging or deploying.
