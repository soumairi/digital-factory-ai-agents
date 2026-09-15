# Quick start: begin a first session in under 10 minutes

With an approved AI tool and repository access already available, you can begin a **synthetic analysis session** in under 10 minutes. Completing project onboarding, the nine-case evaluation suite and an implementation review takes longer; this is not permission to skip them.

1. **Clone the foundation** from your maintainer-provided URL, or use an existing approved snapshot. Verify its release/commit; do not invent a URL or assume a version tag exists.
2. **Choose Backend** using its [README](../agents/backend/README.md).
3. **Choose Laravel** using its [profile](../agents/backend/stacks/laravel/README.md).
4. **Initialize project context** with the [bootstrap script](11-project-agent-bootstrap.md): from the foundation checkout run `./scripts/init-project-agent.sh backend laravel /path/to/project --dry-run`, inspect the plan, then run without `--dry-run`. The target must be an existing project outside the foundation checkout. Use the manual template copy only when the script is unavailable. For a first conversation, use the fictional [Customer Portal example](examples/backend-laravel-agent-example.md) and explicitly flag remaining unknowns.
5. **Start your approved AI tool**, in chat or restricted coding mode.
6. **Load the instructions** from the generated `.ai/README.md` paths (`foundation/backend/core/` and `foundation/backend/laravel/` for bootstrap installs), and use the [bootstrap prompt](04-use-agent-with-chat-ai.md#reusable-bootstrap-prompt). Confirm it received the full shared/core/profile/context documents.
7. **Give one small story:** “As an administrator, I want to list customers with pagination.” Supply the example access and response requirements.
8. **Review the plan.** Expect understanding, missing information, assumptions and security considerations before code.
9. **Let the agent implement only after readiness gates are met:** completed required context, approved story, isolated environment, applicable evaluation evidence and required approvals. Without those, stop at the plan. In chat-only mode, code is a proposal and tests remain NOT RUN until executed.
10. **Review the result** with actual test evidence, independent Security/Audit review and human review. Do not merge or deploy through the agent.

Never paste passwords, tokens, private keys or production credentials into AI tools. Use approved secret-management and sensitive-information channels. No orchestration platform, framework installation or broad production permissions are needed for this first analysis.

Next: [project setup](03-create-project-agent.md), [chat example](examples/chat-session-example.md), or [coding example](examples/coding-agent-example.md).
