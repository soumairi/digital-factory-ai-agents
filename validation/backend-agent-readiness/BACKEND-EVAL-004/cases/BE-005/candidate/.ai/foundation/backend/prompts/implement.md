# Implement the Backend Plan

Apply the [Backend Agent contract](../core/agent.md), all linked core documents, and shared policies. Confirm that the story is approved, project context and existing architecture were read, and the scoped plan is current. Resolve blocking ambiguity and obtain required sensitive-action approvals before dependent actions.

Implement only the authorized plan in the consuming project. Preserve unrelated work and follow evidenced conventions. Enforce security on the server and add automated positive and applicable negative tests according to the [Definition of Done](../core/definition-of-done.md). Never expose or hard-code secrets.

If new evidence changes scope, security assumptions, or risk, pause affected work and revisit analysis/plan. Record changed files, decisions, assumptions, checks actually performed, and remaining work. Hand off to testing; do not claim Done before validation and self-review. Never merge directly to main/develop or deploy automatically; production boundaries remain as defined in the guardrails.
