# Security Output Contract

Follow [shared output standards](../../shared/output-standards.md). Include:

1. **Scope:** story, endpoints/components, exact reviewed revision, environment, policy/context revisions, reviewer identity, authorship separation, and exclusions.
2. **Coverage and evidence:** one entry for every vulnerability-checklist item with outcome, rationale, source references, and verification results. Include the access matrix and negative-test evidence, commands actually run, expected/observed behavior, and skipped checks with reasons. Exclude credentials from evidence.
3. **Findings:** use the record below for every finding; retain stable IDs across revisions.
4. **Gate assessment:** `BLOCKED`, `INCOMPLETE`, or `ELIGIBLE FOR HUMAN REVIEW`, with severity/status counts and reasoning under the shared gate. Incomplete required verification cannot yield eligibility. Eligibility is not story approval.
5. **Handoff:** remediation work, outstanding governance decisions, Audit evidence references, limitations, and human decisions needed.

## Finding record

| Field | Required content |
| --- | --- |
| Finding ID | Stable identifier, for example SEC-001. |
| Affected story | Story identifier/reference. |
| Affected endpoint/component | Operation, route or component and relevant code/configuration reference. |
| Severity | Critical / High / Medium / Low, with rationale under shared policy. |
| Vulnerability or risk | Concrete violated boundary or unsafe behavior. |
| Evidence / reasoning | Revision-bound observations, safe reproduction, source/test references, and explicit inference or uncertainty. |
| Impact | Affected actors/data/assets and plausible consequences. |
| Recommended remediation | Specific corrective outcome without prescribing an unapproved stack. |
| Verification criteria | Observable checks needed to demonstrate the issue is resolved. |
| Status | OPEN / REMEDIATED / ACCEPTED_RISK / FALSE_POSITIVE only. |

Also record owner, status/severity history, reviewer identity, timestamps, and applicable human decision references. Use the [shared governance rules](../../shared/security-development-policy.md#security-gate-and-finding-governance) for transitions. A proposed fix is still OPEN until independent verification succeeds. ACCEPTED_RISK is not a technical fix and cannot clear an unresolved Critical/High issue.
