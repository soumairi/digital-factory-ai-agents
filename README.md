# Digital Factory AI Agent Foundation

Reusable, versioned policies and agent-definition foundations for software projects across a Digital Factory.

This repository is currently a policy and agent-definition foundation, not a collection of executable agents. Version `0.1.0` establishes shared policies and reserves space for future definitions. It includes no orchestration framework, runtime integration, stack-specific rules, project-specific rules, or dependencies.

## Inheritance model

```text
Global Foundation
+ Stack Profile
+ Project Context
= Project Agent
```

- **Foundation** = rules reusable across multiple projects: shared policies and, later, generic role definitions.
- **Stack Profile** = reusable specialization for a technology stack, defined separately from generic role rules. No profiles are implemented yet.
- **Project Layer** = rules valid only for one project, including its context, constraints, conventions, and approval assignments. Keep these in the consuming project's repository.
- **Project Agent** = the resulting combination, consumed by a selected tool or runtime. Composition and execution are outside this initial release.

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
│   │   ├── core/
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

`shared/` contains the policies applicable to every future role. `agents/` reserves role boundaries; backend core definitions and stack profiles have separate locations. Security and Audit are independent second-line control roles, separate from implementation roles.

`project-template/` is reserved for a generic project-context template; `workflows/` for process definitions; `evals/` for policy and behavior evaluations; and `scripts/` for supporting utilities. These directories are empty except for `.gitkeep` files used to preserve them in Git. Their presence does not introduce an implementation commitment.

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

## Initial scope

This release creates the structure and initial shared policies only. Agent definitions, stack profiles (including Laravel), project templates, workflows, evaluations, scripts, and runtime integrations require a separately authorized phase.
