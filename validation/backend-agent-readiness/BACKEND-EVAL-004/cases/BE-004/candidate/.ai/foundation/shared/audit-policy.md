# Audit Policy

Security and Audit form an independent second line of control, separate from implementation roles.

- **Security** reviews technical security risks, control design, and remediation evidence.
- **Audit** reviews policy compliance, approval records, traceability, and whether required controls were followed.
- Neither role may approve its own implementation work or serve as the sole independent reviewer of work it authored. Assign a separate reviewer if either role contributes a fix.
- Use read-only access by default. Review authority does not confer implementation, merge, deployment, or human risk acceptance authority.
- Preserve findings independently of implementation decisions. Implementation roles must not erase, downgrade, or close independent findings unilaterally.
- Record review scope, artifact revision, evidence examined, findings, limitations, and reviewer identity or role.
- For each finding, record impact, supporting evidence, recommended action, owner, and status. Avoid including sensitive data in evidence.
- Require independent verification before closing a finding. Escalate disputes and unresolved material findings to the authorized human owner.
- Missing required approval or unresolved material findings block the affected action. A review opinion cannot replace human approval.
- Review changes to shared security, approval, and audit controls independently before human integration approval.

## Further definition

- **TBD:** Review assignment rules and how future runtimes will enforce reviewer separation and evidence integrity.
- **TBD:** Audit cadence, evidence retention, finding severity, and escalation timelines.
- **Project layer responsibility:** Assign independent reviewers and human escalation owners before controlled work begins.

If an independent reviewer is unavailable, report the control gap and pause work that requires independent clearance.
