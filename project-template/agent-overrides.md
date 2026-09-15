# Agent Overrides — Additions and Explicit Requests

GLOBAL FOUNDATION remains authoritative. PROJECT-SPECIFIC rules may add constraints or select supported conventions. “Override” does not mean last-file-wins or permission to weaken security silently.

## Additive rules

| ID | Affected foundation rule / version | Additional project constraint | Justification | Owner / review reference |
| --- | --- | --- | --- | --- |
| [TBD or none] | [reference] | [constraint] | [reason] | [reference] |

## Conflicts and exception requests

Stop work dependent on a conflict. An exception is a request until approved by an authorized human **and permitted by the governing foundation policy**. Human approval alone cannot waive an absolute prohibition or create exception authority where none exists.

For each request record:

- Exception ID, owner, status (REQUESTED / APPROVED / REJECTED / EXPIRED), and affected rule/version.
- Exact project scope, affected actions/resources, and documented justification.
- Risk description, affected assets and impact.
- Compensating controls and verification evidence.
- Foundation policy clause permitting this exception; if absent, mark blocked and propose a foundation policy PR for human review and versioned adoption before proceeding.
- Independent Security assessment and Audit evidence references.
- Explicit human approval record, approver authority, decision date and conditions.
- Expiration and/or review date and triggering changes; if a fixed expiry is inappropriate, record why and specify a review trigger.
- Remediation/exit plan, renewal owner, and status history.

Unresolved Critical/High findings, agent merges to main, agent production deployment and other absolute inherited prohibitions cannot be bypassed through this file. Permitted Medium/Low risk acceptance follows shared policy; it is not a blanket policy waiver. Expired, unapproved, or out-of-scope exceptions cannot be relied upon. Never auto-carry an exception across a foundation update: reassess its rule version and validity.
