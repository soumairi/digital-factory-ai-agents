# BACKEND-EVAL-002 frozen Foundation

| Component | Frozen reference |
|---|---|
| Foundation | 0.6.0 working-tree bytes, including uncommitted framework hardening |
| Backend Core | agents/backend/core/; v0.1 role definition |
| Laravel profile | agents/backend/stacks/laravel/; v0.1 |
| Specifications | evals/backend/BE-001 through BE-009 |
| Reviewer definitions | evals/backend/fixtures/BE-001.json through BE-009.json; fixture_version1.0.0 |
| Protocol/schema/checker | docs/14-backend-evaluation-protocol.md; evals/backend/README.md, schema/, verify.py |
| Security/Audit | shared/security-development-policy.md; shared/audit-policy.md |
| Exact source inventory | foundation-sha256.json; content hashes, not Git HEAD alone |

The 0.6.0 changes are present but uncommitted. Git HEAD alone identifies an older tracked state; working-tree hashes are the authoritative campaign freeze. No version bump or source edit is authorized. Any change to frozen files/inventory invalidates and stops the campaign. Historical BACKEND-EVAL-001 is separately pinned and remains untouched.
