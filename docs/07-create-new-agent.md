# 7. Create a new agent type

Add a role only when its responsibility is distinct and reusable across projects. Frontend, QA, DevOps, Architecture and Tech Lead are possible future roles; names are not evidence that a definition already exists. This guide does not create them.

Start with a mission such as “Verify an approved change against acceptance criteria and report test evidence.” Define what the role receives, does and produces before selecting a runtime.

```text
agents/<agent-name>/
├── README.md
├── agent.md
├── responsibilities.md
├── workflow.md
├── guardrails.md
├── definition-of-done.md
└── output-contract.md
```

| File | What to write |
| --- | --- |
| README.md | Purpose, scope, version introduction and links to governing documents. |
| agent.md | Mission, required inputs, outputs and authority. |
| responsibilities.md | Work owned by this role and boundaries with other roles. |
| workflow.md | Steps, evidence and conditions for progressing or stopping. |
| guardrails.md | Role-specific limits, referencing shared controls rather than copying them. |
| definition-of-done.md | Observable completion criteria and required validation. |
| output-contract.md | Report fields needed by the next reviewer. |

This is a recommended layout for a new role, not a request to reorganize existing Backend, Security or Audit files.

## Drafting checklist

- State a clear mission and explicit non-goals.
- Define inputs, outputs and evidence references.
- Describe permitted tool capabilities and least-privilege scope, without granting credentials.
- Reference prohibited actions and human approval boundaries.
- State security responsibilities and independent review boundaries.
- Define Done and what missing context/evidence blocks.
- Add evaluation cases for success, failure, misuse, unauthorized actions and scope expansion.
- Keep project facts and framework details out of a generic core.

Propose the documents in a foundation PR. Check overlap with existing roles, evaluate them with controlled fixtures, obtain required independent/human review and release through the [version process](09-update-foundation.md). A DevOps role does not gain production deployment authority because of its name.
