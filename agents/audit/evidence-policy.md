# Audit Evidence Policy

Apply the [shared audit policy](../../shared/audit-policy.md) and [output standards](../../shared/output-standards.md). This document defines how Audit assesses evidence, not a new storage system.

## Evidence record

For each item record a stable evidence ID, source/reference, artifact or policy revision, producer/reviewer identity where relevant, event time and collection time, scope/environment, collection method, and the claim it supports. Include immutable commit IDs, CI run IDs, or document revisions when available. Record integrity information such as a digest when supplied by the approved process; do not invent it.

Prefer primary records: versioned diffs, PR/review metadata, CI execution artifacts, test reports, Security reports and verification records, approval records, and authorized release logs. Agent summaries and screenshots may supplement these but cannot alone prove execution, identity, or authority when required primary evidence is absent. A test file's existence does not prove it ran; a passing run for another revision does not automatically validate this one.

## Sufficiency and handling

- Verify relevance to the scoped story, revision, environment, and policy version. Correlate conflicting sources and record discrepancies.
- Check origin, completeness, readability, and revision integrity. Inaccessible, stale, unverifiable, or contradictory records remain evidence gaps until resolved.
- Link approval records to a specific action/target, authorized approver, conditions, and time. Verify risk decisions and exceptions were valid for the applicable stage and scope.
- Preserve source records; audit reports reference rather than rewrite them. Append corrections and history instead of silently replacing conclusions.
- Redact secrets and minimize personal/confidential data while retaining enough context to assess the claim. Use authorized evidence locations and access controls.
- Record missing evidence, its owner if known, why it matters, and how to obtain it. Lack of access is not non-applicability.
- NOT_APPLICABLE requires a policy/stage-specific rationale. Unperformed required checks remain missing or failed, never implicitly passed.

**TBD in shared governance:** retention duration, evidence store, access roles, and audit cadence. Consuming projects must define these before activities that depend on them. Do not create an unapproved external store or retain sensitive copies to work around undefined governance.
