# Audit Checklist

For each row record PASS / FAIL / MISSING_EVIDENCE / NOT_APPLICABLE, policy reference, evidence IDs, observations, and rationale. Assess applicability for the declared lifecycle stage; no silent omissions.

| Check | Evidence question |
| --- | --- |
| Story-to-implementation traceability | Is the approved User Story linked to acceptance criteria, scoped changes, and implementation revision? |
| Branch / commit traceability | Are branch, commits, diff, authorship, and target branch identifiable and consistent with Git policy? |
| Pull Request existence | Does the required PR exist and reference the correct story, commits, and target? |
| Reviewer identity | Are reviewers identifiable, assigned appropriately, and independent of the work they validate? |
| Automated test execution | Do primary execution records show which commands/tests ran, when, where, and against which revision? |
| Test results | Are outcomes and required positive/negative coverage evidenced, with failures and skipped checks disclosed? |
| Security review | Is there an independent, revision-matched Security report with required coverage, limitations, and gate reasoning? |
| Unresolved findings | Are Security finding IDs/status/history traceable and Critical/High blockers enforced? Is Medium/Low governance evidenced? |
| Approvals | Are approvals required at this stage explicit, action-specific, timely, and issued by authorized humans? Is final approval still pending clearly distinguished? |
| Architecture decisions | Are applicable architecture changes, rationale, and required reviews recorded without inventing unnecessary decisions? |
| Documented exceptions | Are exceptions/risk acceptances authorized, scoped, justified, current, and permitted by shared policy? |
| Deployment/release traceability | Where applicable, do authorized release/deployment records map to approved revisions and actors without prohibited agent actions? |

Audit verifies the existence and sufficiency of technical review evidence; it does not substitute its own vulnerability checklist. A technical concern is referred to Security and tracked as a dependency. Missing evidence for a required check prevents a supported-compliance conclusion.
