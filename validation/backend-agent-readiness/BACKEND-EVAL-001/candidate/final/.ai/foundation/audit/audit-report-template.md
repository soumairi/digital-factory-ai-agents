# Audit Report

Replace placeholders with evidence-backed content. Use `none` for empty sections; do not leave a blank field that could imply a pass.

## Scope

- Audit ID, date, auditor identity, and independence/assignment evidence: [reference]
- Story/change, branch/commits, PR, and exact artifact revision: [references]
- Lifecycle stage, environment, governing foundation/project policy revisions: [references]
- Included activities, exclusions, and limitations: [details]

## Evidence reviewed

| Evidence ID | Source / immutable reference | Revision / scope | Producer / identity | Event / collection time | Claim supported / limitations |
| --- | --- | --- | --- | --- | --- |
| [E-001] | [reference] | [details] | [identity] | [times] | [details] |

## Checks performed

Include every audit-checklist row.

| Check / policy reference | Evidence IDs | Observations | Result | Rationale |
| --- | --- | --- | --- | --- |
| [check] | [IDs] | [facts] | [PASS / FAIL / MISSING_EVIDENCE / NOT_APPLICABLE] | [reason] |

## Findings

Record process/evidence findings here; reference Security IDs rather than duplicate technical findings.

| Audit finding ID | Policy / gap | Evidence / reasoning | Impact / risk rationale | Required corrective evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| [AUD-001] | [gap] | [IDs or missing evidence] | [impact] | [criteria] | [owner/unknown] | [OPEN / VERIFIED_CLOSED] |

Closure requires an independent evidence recheck with reviewer, date, and references. It does not close a linked Security finding.

## Exceptions

| Exception / Security finding ID | Policy basis | Authorized human / authority evidence | Scope / rationale | Conditions / expiry | Decision reference / validity |
| --- | --- | --- | --- | --- | --- |
| [ID or none] | [policy] | [reference] | [details] | [conditions] | [reference] |

An exception is not an agent approval and cannot bypass shared prohibitions or unresolved Critical/High security gates.

## Missing evidence

| Missing item | Affected check / conclusion | Owner | Required next action |
| --- | --- | --- | --- |
| [item or none] | [effect] | [owner/unknown] | [action] |

## Risk level

[Critical / High / Medium / Low / Undetermined], with evidence-based rationale, uncertainty, and applicable project risk criteria. Do not use missing evidence to justify Low risk. Keep audit process risk separate from Security vulnerability severity; do not recalculate or downgrade Security findings. If criteria or evidence are insufficient, use Undetermined and explain.

## Conclusion

Choose one and justify it against the checks:

- **SUPPORTED WITHIN SCOPE:** required checks are evidenced and satisfied for this stage; permitted exceptions are explicit. This is not final human approval or a claim beyond the stated scope.
- **NONCONFORMING:** evidence demonstrates a policy violation; identify blocking findings and remediation.
- **INSUFFICIENT EVIDENCE:** required evidence cannot support a conclusion; identify missing records and blocked decisions.

If violations and evidence gaps coexist, use NONCONFORMING and retain all evidence limitations. State the Security gate result/reference, unresolved findings, required human decisions, and any pending later-stage audit. Stop at human handoff; do not merge or deploy.
