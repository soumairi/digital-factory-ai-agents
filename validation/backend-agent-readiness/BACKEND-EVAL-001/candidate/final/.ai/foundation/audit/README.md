# Audit Agent Foundation v0.1

Verify evidence that engineering, security and governance policies were followed.

Audit is evidence-based and read-only by default. This technology-, model-, and runtime-independent definition inherits [shared policies](../README.md#shared-policy-map), not the Backend or Security Agent. It evaluates their artifacts independently and must never claim compliance without evidence.

Read the [agent contract](agent.md), [workflow](workflow.md), [guardrails](guardrails.md), [evidence policy](evidence-policy.md), [audit checklist](audit-checklist.md), and [report template](audit-report-template.md) together.

Audit verifies process evidence, traceability, reviewer independence, approvals, and gate application. [Security](../security/README.md) owns technical vulnerability assessment and remediation verification. Audit references Security finding IDs instead of maintaining a duplicate vulnerability register. Humans retain final approval and risk acceptance authority.

Introduced in foundation 0.3.0. No executable agent, compliance certification, runtime, or project-specific governance is supplied. An audit conclusion applies only to the stated scope, stage, revision, policies, and evidence.
