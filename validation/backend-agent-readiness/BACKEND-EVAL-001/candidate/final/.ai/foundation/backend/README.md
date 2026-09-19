# Backend Agent Foundation v0.1

> Transform an approved User Story into a secure, maintainable, tested backend implementation ready for human review.

This is a declarative role definition and a set of reusable prompts, not an executable agent. The core assumes no language, backend framework, AI model, tool, or orchestration runtime.

## Composition and authority

Global Foundation (shared policies + backend core) + Stack Profile + Project Context = Project Agent.

Read every [shared policy](../README.md#shared-policy-map) and the core documents before applying a prompt. Shared policies remain authoritative; this role adds stricter backend boundaries. Stack profiles and project context may specialize or tighten controls, never weaken them. Flag conflicts for human resolution.

Project context must supply the approved story, acceptance criteria, architecture references, verified conventions, allowed environment, test commands, and approval/reviewer assignments. Discover these from authorized project sources; never invent them. Missing information blocks dependent work, not unrelated authorized inspection.

## Documents

- [Agent contract](core/agent.md): mission, inputs, outputs, and authority.
- [Responsibilities](core/responsibilities.md): implementation ownership and review separation.
- [Workflow](core/workflow.md): lifecycle and progression gates.
- [Guardrails](core/guardrails.md): mandatory boundaries.
- [Definition of Done](core/definition-of-done.md): acceptance, security, and test evidence.
- [Output contract](core/output-contract.md): technical report for human review.

Use the prompts in lifecycle order: [analyze](prompts/analyze.md), [plan](prompts/plan.md), [implement](prompts/implement.md), [test](prompts/test.md), and [self-review](prompts/self-review.md). Each prompt requires the full governing context; it is not a standalone permission grant. Revisit earlier stages when evidence changes.

The [Laravel profile](laravel/README.md) extends Backend Core with framework-specific guidance. Django, FastAPI, and Node directories remain README placeholders and supply no implementation conventions.

## Version and scope

Backend definition version: **0.1**, introduced in repository foundation **0.2.0**. Pin the repository release to reproduce the definition and shared policies together; the role label is descriptive, not a separate release mechanism.

The core remains technology-agnostic; implemented stack guidance lives only in the separate Laravel profile. This foundation contains no project rules, runnable agents, dependencies, or runtime adapters. Policy text requires enforcement by future consuming environments. The lifecycle ends at human review; it does not authorize merge or deployment.
