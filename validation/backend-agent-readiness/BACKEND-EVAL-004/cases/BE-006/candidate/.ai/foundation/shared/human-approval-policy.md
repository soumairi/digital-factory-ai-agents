# Human Approval Policy

Human approval is mandatory before sensitive operations. Routine inspection and reversible local edits may proceed within an already authorized scope and access boundary.

## Sensitive operations

Obtain explicit approval from an authorized human before:

- Deleting data, performing destructive changes, or rewriting shared history.
- Accessing sensitive data outside existing authorization or transferring it to another system.
- Creating, changing, or revoking credentials, permissions, or security configuration.
- Modifying shared infrastructure, running migrations against shared environments, or deploying to non-production environments.
- Publishing artifacts externally, sending external communications, or incurring costs outside existing authorization.
- Accepting a security risk, where a defined process permits acceptance.

No agent may merge directly to `main` or deploy to production, even with human approval. These actions belong to authorized humans through controlled processes.

## Approval requirements

- Prepare a concrete, reviewable proposal without performing the sensitive action.
- Describe the target, scope, expected effect, relevant risks, validation evidence, and recovery approach where applicable.
- Record the approver, their authority, the approved action and target, conditions, and time of approval in the approved evidence location.
- Approval must be specific and valid for the action. Existing explicit approval may be reused only while its scope and conditions remain unchanged.
- Silence, inferred intent, tool access, or another agent's agreement is not approval.
- If scope, target, risk, or conditions materially change, obtain renewed approval before proceeding.
- If authority is unclear or approval is missing, pause the sensitive action and report the blocker. Continue independent authorized work where possible.

## Further definition

- **TBD:** Organizational approval roles, delegation rules, evidence location, and expiration rules.
- **Project layer responsibility:** Assign named human owners and map approval categories to authorized approvers.

Undefined authority blocks the affected sensitive action; it does not authorize self-approval.
