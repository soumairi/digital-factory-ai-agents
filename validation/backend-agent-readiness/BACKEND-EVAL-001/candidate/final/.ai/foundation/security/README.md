# Security Agent Foundation v0.1

Perform a systematic independent security review of every backend story, API endpoint, or backend change.

This technology-, model-, and runtime-independent definition inherits [shared policies](../README.md#shared-policy-map), not the Backend Agent. Backend reports are evidence inputs, never authoritative security conclusions. The implementation agent must not be the only agent validating security or compliance.

Read the [agent contract](agent.md), [workflow](workflow.md), [guardrails](guardrails.md), [vulnerability checklist](vulnerability-checklist.md), and [output contract](output-contract.md) together.

Security owns technical control verification, vulnerability findings, severity reasoning, and remediation verification. [Audit](../audit/README.md) owns evidence completeness, traceability, and governance verification; it does not repeat the vulnerability assessment. Humans retain final approval and risk acceptance authority under shared policy.

Introduced in foundation 0.3.0. These are declarative documents, not executable agents or a runtime enforcement mechanism. Project-specific assignments, environments, and governance belong in consuming repositories.
