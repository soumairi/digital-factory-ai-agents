# Example: Customer Portal Laravel Backend Agent

This is a fictional learning example, not a ready-made project policy or completed evaluation.

## Project context

Customer Portal uses Laravel and PostgreSQL. Exact versions come from its Composer lockfile and approved database configuration, not this guide. In this fictional project, existing authenticated sessions and a project Policy authorize administrator access; no JWT, Sanctum, Passport or permission package is assumed.

The approved story is: “As an administrator, I want to list customers with pagination.” For this example, administrators may list customers only in their own tenant; non-administrators and anonymous callers are denied. Return only customer ID and display name, ordered by unique customer ID. Default page size is 20, maximum 100; reject invalid pagination parameters. Counts and results must respect the tenant boundary. All data is synthetic. A real project must confirm these requirements and its error/response conventions with its owner.

## Instructions supplied

```text
.ai/foundation/shared/                         # all seven policies
+ .ai/foundation/agents/backend/core/          # all six core documents
+ .ai/foundation/agents/backend/stacks/laravel/ # complete profile
+ .ai/project/                                # completed context and pin
```

Also read the Backend README and relevant stage prompts. Load Security and Audit definitions separately for their assigned reviews. Follow the [project setup guide](../03-create-project-agent.md) to prepare actual source references and evaluation evidence.

## Expected workflow

```text
Analysis → Plan with security considerations → Scoped implementation
→ Feature/unit tests as appropriate → Self-review
→ Independent Security review → Fix/reverify if needed
→ Audit evidence review → Human validation
```

Analysis identifies existing routes, request validation, authorization, query scopes, resources and tests. The plan lists only relevant files and proposes bounded pagination and safe serialization using the actual architecture. It flags unknown conventions before implementation.

Tests check authorized tenant administrators, anonymous/non-admin callers, cross-tenant leakage, invalid page sizes, field visibility and stable pagination. Security independently verifies controls and denied outcomes; Audit checks revision-matched evidence and review/approval records. Proposed or unexecuted tests are not passing evidence.

The final report lists changed files, assumptions, exact tests/results and unresolved risks under the Backend output contract. No full implementation is supplied here because code must follow the actual project. No review result or approval is implied by this example.
