# Laravel Backend Profile v0.1

This profile **extends Backend Core**. It is not a standalone agent and does not replace core or shared policies.

Shared policies + [Backend Core](../README.md) + Laravel profile + project context = project Backend Agent.

Read the full Backend Core and applicable shared policies first, then this profile and the consuming project's context. Specialization may tighten controls but cannot weaken them. Resolve conflicts explicitly before dependent work.

## Inherited versus specialized rules

| Source of authority | Rules owned there |
| --- | --- |
| [Core agent contract](../core/agent.md) and [workflow](../core/workflow.md) | Mission, approved story, context inspection, planning, implementation, testing, self-review, human handoff. |
| [Core guardrails](../core/guardrails.md) | Focused changes, assumptions, secrets, least privilege, approvals, production access, merge and deployment boundaries. |
| [Core Definition of Done](../core/definition-of-done.md) | Full security applicability assessment and automated negative-test gates. |
| [Core output contract](../core/output-contract.md) | Changed files, assumptions, executed tests/results, security evidence and review status. |
| [Shared security development policy](../../shared/security-development-policy.md) | Independent Security/Audit roles, findings governance and human decision gates. |
| This profile | Laravel mechanisms and implementation checks that satisfy those inherited requirements. |

The profile adds no separate lifecycle, report schema, vulnerability register, or approval process. Report Laravel-specific evidence within the core output contract; retain every inherited Done requirement, including security topics not repeated here.

## Profile documents

- [Architecture](architecture.md): discover project structure and keep controller responsibilities small.
- [Coding rules](coding-rules.md): FormRequests and Laravel implementation conventions.
- [Security rules](security-rules.md): authorization, uploads, jobs and configuration.
- [Testing rules](testing-rules.md): feature/unit and negative-test evidence.
- [Database rules](database-rules.md): Eloquent, assignment, queries and transactions.
- [API rules](api-rules.md): resources, pagination and error contracts.
- [Commands](commands.md): illustrative commands and execution gates.

Never assume JWT, Sanctum, Passport, Spatie Permission, Repository Pattern, or Service Pattern. Detect and follow the actual project architecture and configured authentication/authorization mechanisms. Package presence alone does not prove use on an endpoint. Do not add a package or architectural layer to satisfy an assumption.

Laravel profile version **0.1**, introduced in foundation **0.4.0**. No Laravel/PHP version is prescribed: inspect `composer.json`, `composer.lock`, installed capabilities when available, and project instructions. Match official documentation to that version before using APIs. The references below and in the other documents are implementation references, not a project version pin or a compatibility certification.

This is policy content only: no Laravel application, dependencies, runnable agent, or command execution is introduced.
