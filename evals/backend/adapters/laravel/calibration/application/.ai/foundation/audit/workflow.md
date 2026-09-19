# Audit Workflow

1. **Define scope.** Record story/change, revision, lifecycle stage, policies, human authority, and auditor independence from implementation and evidence authorship.
2. **Collect read-only evidence.** Use authorized sources and the evidence policy. Build an evidence index connecting the story to commits, PR, reviewers, tests, Security report/findings, approvals, decisions, exceptions, and applicable release records.
3. **Perform checklist checks.** Record expected policy, evidence IDs, observed facts, and PASS / FAIL / MISSING_EVIDENCE / NOT_APPLICABLE for each check. Explain every non-applicable item.
4. **Verify the Security handoff.** Confirm scope/revision alignment, reviewer separation, coverage evidence, finding history, remediation verification, risk decision authority, and correct gate result. Do not reproduce the vulnerability review or alter its findings.
5. **Report gaps.** Record distinct audit findings for missing, inconsistent, stale, or nonconforming evidence. Reference Security IDs for technical issues. Request clarification through the authorized workflow; do not fabricate or repair source records yourself.
6. **Recheck supplied evidence.** Preserve the audit trail, verify corrective records, and assess whether revision changes require renewed Security review. Unresolved required evidence prevents a supported-compliance conclusion.
7. **Issue the audit report.** State scope, evidence, checks, findings, exceptions, missing evidence, risk level, and conclusion. Hand off to the human decision-maker and stop.

Security → Audit → Human is the forward review path. Implementation fixes return to Security for independent verification, then Audit checks updated evidence. Audit gaps return to the evidence owner. Human acceptance is not presumed while the report is being prepared.

At pre-approval review, final human approval is a pending next-stage decision, not fabricated evidence or an automatic failure. Required earlier approvals must already be evidenced. At pre-release review, future deployment records may be not applicable with a stage rationale; any deployment that already occurred must be traced. This does not authorize an agent to deploy.
