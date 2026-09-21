# Required pilot controls

These controls are mandatory for each project; this package does not record their completion for a real pilot.

1. Explicit human authorization before implementation, with approver authority, scope, target, conditions and timestamp.
2. Complete the Pre-Implementation Gate before bounded Backend Agent work.
3. Freeze each candidate revision and hashes before independent review; refreeze and repeat affected reviews after remediation.
4. Independent Security review for every backend story, endpoint or change; independently verify remediation.
5. Independent Audit review of policy compliance, approvals and traceability according to Foundation policy.
6. Human final approval after Security and Audit gates; no agent deployment to production.
7. No production secrets and no autonomous merge; agents may not merge directly to main.
8. No production database access under RC1. Any separately authorized access requires a separate scope and controls; it does not expand RC1 or permit production writes.
9. Prefer synthetic/test data; isolate secrets and disposable validation environments with external containment.
10. Retain authorization, context, candidate hashes, test logs, findings, review identity and human decisions in an access-controlled evidence location with project-defined retention.
11. Maintain a tested rollback path and stop immediately when required controls or integrity fail.

Follow [Human approval](../../shared/human-approval-policy.md), [Security development](../../shared/security-development-policy.md), [Audit](../../shared/audit-policy.md), and the [Backend workflow](../../agents/backend/core/workflow.md). Unresolved Critical/High findings block approval; risk acceptance cannot clear them. Assign distinct implementer, Security and Audit reviewers; a role-label change is not independence.
