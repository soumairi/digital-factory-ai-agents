# 6. Security and Audit workflow

```text
Backend Agent: Security-by-Default implementation
→ QA / automated tests → Backend self-review
→ Independent Security Agent review
→ Remediation by implementation role → Security verifies fixes
→ Audit Agent verifies evidence and traceability
→ Human approval
```

QA here means testing activity; the repository's QA Agent directory is still a placeholder. It is not an implemented additional reviewer.

| Role | Responsibility |
| --- | --- |
| Backend | First security line: build controls and tests, document assumptions and evidence. |
| Security | Independent second security line: actively verify technical controls, access/ownership boundaries and abuse cases. Working functionality alone is not security proof. |
| Audit | Verify evidence, reviewer identity, traceability, approvals and gate application. Do not repeat or silently reclassify technical findings. |
| Human | Final authority for approval and permitted risk acceptance within global constraints. |

Use the complete [Security definition](../agents/security/README.md) and [Audit definition](../agents/audit/README.md), together with shared policies and project context. Give Security the approved story, precise code revision/diff, tests and configuration evidence. Give Audit the Security report/findings, test runs, PR/commit records, review identities and applicable approvals. Reports must refer to the same revision; changed code needs impact assessment and relevant rechecks.

Separate assignments are required: the implementing agent cannot be its only security/compliance validator. In manual mode, use a distinct review session/agent assigned to Security; Audit must be separate from authorship of the implementation and evidence it audits. Record identities and scope. Changing the implementer's role label is insufficient. A reviewer who authors a fix needs another independent reviewer for that fix. A different model/provider is optional, not proof of independence.

## Gate outcomes

| Finding | Required treatment |
| --- | --- |
| Unresolved Critical | BLOCK approval, regardless of evaluation score. |
| Unresolved High | BLOCK approval. |
| Medium | Documented project governance decision. |
| Low | Documented governance decision and tracking; not silent dismissal. |

The [shared security gate](../shared/security-development-policy.md#security-gate-and-finding-governance) is authoritative. ACCEPTED_RISK is not a fix and cannot clear Critical/High blockers. Medium/Low acceptance requires authorized human decisions where policy permits it; undefined governance blocks approval. Missing verification is not clearance. Audit never claims compliance without evidence.

## Human approval boundaries

The [human approval policy](../shared/human-approval-policy.md) requires explicit authority for destructive operations, shared infrastructure/migrations, credentials/permission/security changes, sensitive data access/transfers beyond authorization, external publication/communications, out-of-scope costs and permitted risk acceptance. Use a concrete proposal with action, target, risks, evidence and recovery approach. Existing valid specific approval need not be requested again, but changed scope needs renewed approval.

No human task approval can authorize an agent to merge directly to main or deploy to production; Backend also prohibits direct main/develop pushes/merges and automatic deployment. Production access requires separate governance, never default tool access. Never paste production credentials, passwords, tokens or private keys into chat; use approved organizational secret and sensitive-data mechanisms.
