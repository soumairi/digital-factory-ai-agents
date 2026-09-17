# Independent Security Review Handoff

Status: **REQUIRED — NOT PERFORMED**. Start in a separate AI session from the Backend implementer. A role switch in the implementation session does not establish independence. Record reviewer/session identity, assignment, date and candidate ID `78fa5b87b156c1201525d3b097fe68f3c46b9d62fe829dd7087dfa80d8b56695`.

## Required inputs

- [Story](../input/story.md)
- [Acceptance criteria](../input/acceptance-criteria.md)
- [Exact frozen security context](../input/project-security-context.md)
- [Candidate identity and verification instructions](../revision/README.md)
- [Artifact SHA-256 inventory](../revision/artifact-sha256.txt) and [compact source snapshot](../revision/candidate.tar.gz)
- [Implementation diff](../revision/implementation.diff) and [changed files](../revision/changed-files.json)
- [Backend summary](../backend/backend-summary.md), [self-review](../backend/backend-self-review.md) and [test summary](../backend/test-results-summary.md)

Verify package and candidate hashes before review; stop on mismatch. Read the frozen `.ai/foundation/security/` and relevant `.ai/foundation/shared/` documents in the snapshot, plus all relevant frozen project context. Backend claims are inputs, not clearance. The original sandbox may be inspected read-only for additional configuration/dependency context; inventory coverage limits are documented in revision/README.md.

The context's no-event-sink wording predates the final denial-event code. Preserve this discrepancy and assess actual evidence; do not rewrite context or reports to hide it. Scope is synthetic, in-process, administrator-global access; do not claim production/TLS, tenant or full-suite assurance.

## Authority and output

**No authority to modify application code**, original evidence, Backend reports or Foundation rules. Review output must be written **only under `validation/runs/US-BE-001/security/`**. Keep this handoff README unchanged; create separate report/findings/evidence files. This package does not authorize a test rerun that writes outside that output boundary; propose any required isolated execution arrangement for the separate session before acting.

Use the frozen Security output contract and finding format. Inspect actual sources, assess every vulnerability-checklist row, distinguish verified/not-verified/non-applicable, and identify revision-bound evidence. Critical/High unresolved findings BLOCK; incomplete verification also prevents clearance. Do not modify code, downgrade issues to pass, accept risk or grant human approval.

Recommended outputs: `security-review.md`, `findings.md`, and review-evidence references under this directory. Record a gate result and Critical/High counts only after review. Remediation belongs to a separately authorized Backend session and creates a new candidate; independent re-verification must explicitly identify that candidate. Never overwrite this frozen revision to represent a fix.
