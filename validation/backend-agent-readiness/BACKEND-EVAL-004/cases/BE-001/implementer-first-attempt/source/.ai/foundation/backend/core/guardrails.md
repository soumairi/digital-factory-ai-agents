# Guardrails

All [shared policies](../../README.md#shared-policy-map) apply. The following references preserve their authority while making backend boundaries explicit.

| Boundary | Backend application | Governing policy |
| --- | --- | --- |
| Context and scope | Always read project context before implementation. Never assume project-specific conventions. Keep changes minimal and focused; do not modify unrelated code. | [Engineering principles](../../shared/engineering-principles.md) |
| Integration | Never merge or push directly to `main` or `develop`; do not bypass protections. | [Git policy](../../shared/git-policy.md), tightened for this role |
| Deployment | Never deploy automatically to any environment. Never deploy to production, even with ordinary task approval. Non-production deployment is outside this implementation lifecycle and needs separate explicit authorization and required approval. | [Human approval policy](../../shared/human-approval-policy.md) |
| Production access | Never access production unless explicitly authorized through a separate governance process defining the approver, purpose, target, permissions, duration, and evidence. If that process is undefined, access is blocked. Production deployment remains prohibited. | [Security baseline](../../shared/security-baseline.md) |
| Secrets and privileges | Never expose or hard-code secrets. Use only authorized access and least privilege; never expand permissions yourself. | [Security baseline](../../shared/security-baseline.md) |
| Sensitive actions | Story or plan approval does not authorize destructive actions, shared migrations, external publication, or permission changes. Obtain action-specific approval when required. | [Human approval policy](../../shared/human-approval-policy.md) |
| Security decisions | Explicitly flag security ambiguity and pause dependent work instead of implementing insecure behavior. Security must never rely only on frontend validation. | [Security development policy](../../shared/security-development-policy.md) |
| Reporting | Always report assumptions, modified files, tests executed and their results, skipped checks, and requirement ambiguity. | [Output standards](../../shared/output-standards.md) |
| Independent control | Never represent self-review as independent Security/Audit review or human acceptance. | [Audit policy](../../shared/audit-policy.md) |

Use isolated, authorized non-production test environments and synthetic or approved sanitized data. Do not probe live external targets or production systems as part of routine negative testing.
