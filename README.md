# Digital Factory AI Agent Foundation

Reusable, versioned policies and agent-definition foundations for software projects across a Digital Factory.

This repository is currently a policy and agent-definition foundation, not a collection of executable agents. Version `0.5.0` includes shared policies, Backend, Security, and Audit Agent foundations, a Laravel Backend profile, reusable project integration templates, and manual backend evaluation specifications. It includes no orchestration framework, runtime integration, project-specific rules, or dependencies.

## Inheritance model

```text
Global Foundation
+ Agent Core
+ Stack Profile
+ Project Context
===============
Project-Specific Agent
```

- **Global Foundation** = shared rules reusable across multiple projects. The repository also versions the cores, profiles, templates and evaluations together.
- **Agent Core** = reusable role mission, responsibilities, lifecycle, guardrails, Done criteria and output contract.
- **Stack Profile** = reusable specialization for a technology stack, defined separately from generic role rules. The [Laravel profile](agents/backend/stacks/laravel/README.md) is implemented; other stack directories remain placeholders.
- **Project Layer** = rules valid only for one project, including its context, constraints, conventions, and approval assignments. Keep these in the consuming project's repository.
- **Project-Specific Agent** = the resulting combination, consumed by a selected tool or runtime. Composition and execution are outside this initial release.

Specialization adds context and may tighten controls; it must not weaken shared security, least-privilege, approval, or independence requirements. Stop and seek human resolution when rules conflict. A human approval cannot authorize an agent to merge directly to `main` or deploy to production.

The foundation is independent of AI models and coding tools. Its plain-text definitions are intended for future use with Codex, Claude Code, Cursor, OpenAI Agents SDK, or other runtimes. No integration or compatibility validation is provided in this release. Runtime permissions and repository controls must eventually enforce the policies; Markdown alone does not enforce them.

## Repository layout

```text
digital-factory-ai-agents/
├── README.md
├── VERSION
├── CHANGELOG.md
├── shared/
│   ├── engineering-principles.md
│   ├── security-baseline.md
│   ├── security-development-policy.md
│   ├── git-policy.md
│   ├── human-approval-policy.md
│   ├── audit-policy.md
│   └── output-standards.md
├── agents/
│   ├── backend/
│   │   ├── README.md
│   │   ├── core/
│   │   ├── prompts/
│   │   └── stacks/
│   ├── frontend/
│   ├── qa/
│   ├── security/
│   ├── audit/
│   ├── architecture/
│   └── devops/
├── project-template/
├── workflows/
├── evals/
└── scripts/
```

`shared/` contains the policies applicable to every future role. `agents/` separates role boundaries; the [Backend Agent Foundation](agents/backend/README.md) contains technology-agnostic core definitions and reusable lifecycle prompts, with a separate Laravel specialization and placeholders for other stacks. [Security](agents/security/README.md) independently verifies technical security controls; [Audit](agents/audit/README.md) verifies evidence, traceability, and governance. Both are separate from implementation roles, and humans remain the final approval authority.

`project-template/` contains [copyable project context templates](project-template/README.md) and a foundation version pin. `evals/backend/` contains [nine evaluation cases and the common scoring/maturity model](evals/backend/README.md). These are specifications, not an executable harness. `workflows/` and `scripts/` remain reserved directories retained by `.gitkeep` files.

## Shared policy map

| Policy | Scope |
| --- | --- |
| [Engineering principles](shared/engineering-principles.md) | Maintainable, scoped, verifiable engineering |
| [Security baseline](shared/security-baseline.md) | Least privilege, data protection, and trust boundaries |
| [Security development policy](shared/security-development-policy.md) | Security responsibilities during development |
| [Git policy](shared/git-policy.md) | Reviewable changes and protected integration |
| [Human approval policy](shared/human-approval-policy.md) | Sensitive actions and approval evidence |
| [Audit policy](shared/audit-policy.md) | Independent review, findings, and traceability |
| [Output standards](shared/output-standards.md) | Clear deliverables, evidence, and limitations |

## Versioning and evolution

`VERSION` identifies the foundation release; `CHANGELOG.md` records changes. Use semantic versioning: major for incompatible policy or composition changes, minor for compatible additions, and patch for compatible corrections. During `0.x`, incompatible changes increment the minor version and must be identified explicitly in the changelog. Consumers should pin a release and review changes before upgrading.

Project-specific knowledge stays in the project layer. A lesson may be proposed for promotion only after removing project details and secrets and demonstrating its usefulness across projects. Promotion requires human review, independent Security/Audit review when controls are affected, and a versioned foundation change. It is never automatic.

`TBD` identifies a decision still required before the related capability is used. It is not an exemption from an existing rule. Where required authority or controls are undefined, the affected sensitive action must remain blocked.

## Current scope

This release includes shared policies and declarative Backend, Security, and Audit Agent foundations. The Laravel profile extends Backend Core. Project integration templates and manual backend evaluation specifications are included. Other stack profiles, additional roles, shared workflows, executable evaluation fixtures/harnesses, scripts, and runtime integrations require a separately authorized phase.

## Project consumption and feedback

For a new Laravel project, copy `project-template/` into the project repository and fill its context from actual code and approved requirements. Obtain a reviewed foundation snapshot, record its exact version in `FOUNDATION_VERSION` and immutable source in project-context.md, and combine shared policies, Backend Core, the Laravel profile and completed project context. The Security and Audit roles consume their own independent definitions and the same governing context; they do not inherit implementation authority. See the [integration steps](project-template/README.md).

```text
Project experience
→ Lessons learned
→ Foundation Pull Request
→ Evaluation
→ New Foundation version
→ Adoption by projects
```

Keep project-specific experience local. Generalize useful lessons, remove secrets and identifying project details, and propose a focused foundation PR. Evaluate the candidate with relevant cases and regressions, obtain independent review for affected controls and human review, then release through the defined human-controlled process. Agents do not merge directly or publish a release implicitly.

Updates are opt-in: each project reviews changes, reassesses exceptions, evaluates the candidate with its own context, and adopts through a human-reviewed project PR updating both snapshot/reference and version pin. No automatic synchronization with main. Preserve the previous version and evidence for rollback.

Before a first real Backend Agent trial, supply a consuming repository, completed context, approved story, concrete evaluation fixtures/assertions, safe commands and an isolated environment. Select/configure a runtime with enforced permissions and assign independent Security/Audit reviewers and human authorities. Run the initial nine-case suite and inspect failures before claiming readiness. Scores and maturity never authorize autonomous production deployment.
