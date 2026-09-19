# Developer documentation

Start with the [quick start](quick-start.md) to begin a synthetic analysis session, or read the guides in order. An agent here is a written definition that a chosen AI runtime follows; no separate “Agentic AI” platform is required.

These guides explain existing behavior. The pinned shared/core/profile policies remain authoritative; examples are fictional, not new project rules or approval records. **Required** steps follow those policies. **Optional** choices include the runtime, UI method, snapshot location and tool-specific loading convenience.

## Guides

- [Agentic AI basics](01-agentic-ai-basics.md)
- [Foundation architecture and rule priority](02-foundation-architecture.md)
- [Create a project agent](03-create-project-agent.md)
- [Use with conversational AI](04-use-agent-with-chat-ai.md)
- [Use with coding AI](05-use-agent-with-coding-ai.md)
- [Security, Audit and human approval](06-security-and-audit-workflow.md)
- [Create a new agent type](07-create-new-agent.md)
- [Create a stack profile](08-create-stack-profile.md)
- [Update and adopt the foundation](09-update-foundation.md)
- [Team workflow and remaining setup](10-team-workflow.md)

- [Project agent bootstrap](11-project-agent-bootstrap.md)

## Examples

- [Laravel Backend Agent](examples/backend-laravel-agent-example.md)
- [Manual chat session](examples/chat-session-example.md)
- [Repository-aware coding agent](examples/coding-agent-example.md)

## What is ready and what is not

The repository provides Backend, Security and Audit definitions, a Laravel profile, project templates and evaluation specifications. Other role/stack placeholders are not implemented agents. There is no automatic loader, executable harness or orchestration framework. Teams supply their actual context, approved runtime/permissions, fixtures, review assignments and evidence.

Never put production credentials, passwords, tokens or private keys in conversational tools or context documents. Use approved organizational mechanisms for secrets and sensitive information. See [human approval boundaries](06-security-and-audit-workflow.md#human-approval-boundaries).

[Return to repository README](../README.md).

- [Update an installed project Foundation](12-update-project-foundation.md): preview, integrity checks, backups, force and rollback without replacing project context.

- [Backend evaluation protocol](14-backend-evaluation-protocol.md): reviewer fixtures, L1 independence, evidence and sensitivity gates.
