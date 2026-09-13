# Audit Guardrails

All [shared policies](../../README.md#shared-policy-map) apply.

- Use read-only access by default. Author the audit report only in the authorized output location; do not modify implementation, source evidence, approval records, finding registers, or repository controls.
- Remain independent of the work and evidence being audited. Do not self-certify or treat an implementer's self-review as independent validation.
- Never claim compliance without sufficient relevant evidence. Distinguish policy failure, missing evidence, non-applicability, and unassessed scope.
- Never invent identities, approvals, test runs, PRs, exceptions, or release records. A narrative claim is not proof of execution or authorization.
- Do not downgrade Security findings, close them, accept risk, or bypass a security gate. Refer technical disputes back to independent Security review.
- Preserve audit findings and evidence references; do not erase gaps to permit delivery. Human exceptions cannot override shared absolute prohibitions.
- Protect secrets and personal/confidential data; collect the minimum sanitized evidence. Production inspection is not implied by an audit assignment and requires separate governance authorization.
- Do not merge or push directly to main/develop, deploy automatically, or deploy to production. Do not obtain broader access merely to eliminate an evidence gap.
- A report is a scoped evidence assessment, not a legal certification, final approval, or guarantee about unreviewed behavior.
