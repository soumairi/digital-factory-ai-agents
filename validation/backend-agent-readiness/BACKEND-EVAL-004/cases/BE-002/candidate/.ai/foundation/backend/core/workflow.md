# Workflow

User Story → Understand requirement → Inspect project context → Inspect existing architecture → Identify risks and assumptions → Produce implementation plan → Implement → Run tests → Perform self-review → Produce technical report → Human review

| Stage | Required action and evidence | Progression gate |
| --- | --- | --- |
| User Story | Identify approved story, scope, acceptance criteria, and approval reference. | No implementation without an approved story. |
| Understand requirement | Map expected behavior and failure cases; flag ambiguity. | Resolve ambiguity before work that depends on it. |
| Inspect project context | Read applicable instructions, allowed environments, conventions, security expectations, and validation commands; record sources. | Never assume project-specific conventions. |
| Inspect existing architecture | Trace affected entry points, services, persistence, access controls, and tests. | Identify the existing boundaries and integration points before designing changes. |
| Identify risks and assumptions | Assess every security topic in the Definition of Done; record assumptions and open decisions. | Security ambiguity blocks dependent implementation; do not choose permissive defaults. |
| Produce implementation plan | Map acceptance criteria to changes and tests, expected files, security controls, compatibility/data impacts, and required approvals. | Stay within story authorization; obtain specific approval for sensitive actions under shared policy. |
| Implement | Apply the minimal scoped plan in the consuming project, with tests and relevant documentation. | Revisit analysis and plan when scope or risk changes; do not modify unrelated code. |
| Run tests | Execute authorized positive, negative, regression, and relevant security checks; preserve results. | Missing or failing required checks prevent a Done claim. |
| Perform self-review | Review the final diff against acceptance criteria, guardrails, and every Done gate; fix findings and rerun affected checks. | Self-review cannot replace independent review. |
| Produce technical report | Use the output contract, including modified files, assumptions, test results, security evidence, and review needs. | Report incomplete or blocked work explicitly. |
| Human review | Hand off the implementation and evidence, including required independent Security/Audit review status. | Stop; do not merge or deploy. |

Required independent reviews follow the [security development policy](../../shared/security-development-policy.md) and [audit policy](../../shared/audit-policy.md). A report may be submitted with unresolved issues, but must not label the work Done while required gates remain unmet.
