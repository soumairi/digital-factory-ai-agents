# Pilot entry criteria

All items require project-specific evidence before implementation:

- [ ] Project owner explicitly approves the pilot and its bounded scope.
- [ ] Repository is non-production or controlled staging; validation is disposable and contained.
- [ ] Project context and Security context are documented.
- [ ] Stack is Laravel; approved Foundation 0.6.1 is installed and verified against the RC freeze.
- [ ] Project-specific `.ai/project` exists; initialize using the [bootstrap instructions](../../docs/11-project-agent-bootstrap.md).
- [ ] Secrets are isolated; production deployment is disabled; production credentials/data access are absent.
- [ ] Named human reviewer and authorized final approver are assigned.
- [ ] Independent Security reviewer is assigned (required for every backend change).
- [ ] Independent Audit reviewer is available and assigned before required clearance.
- [ ] Rollback path exists and logging/evidence storage and retention are defined.
- [ ] Pre-Implementation Gate is completed; candidate freeze and review sequence are planned.
- [ ] PostgreSQL projects complete target-engine validation before pilot entry and any database-sensitive story. RC1's SQLite evidence cannot satisfy this requirement.

Use the [pilot templates](../../project-template/pilot/pilot-authorization.md). Empty checkboxes and template placeholders are not approvals.
