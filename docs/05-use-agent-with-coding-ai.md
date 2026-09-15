# 5. Use an agent with a repository-aware coding tool

A repository-aware tool can inspect project files and, when configured, use Git, a terminal, tests and linters. Codex, Claude Code, Cursor and other coding agents are examples; the definition does not depend on them. Check your installed tool's actual capabilities and organization settings instead of assuming identical access or instruction loading.

## Required setup

Prepare the [project structure](03-create-project-agent.md), approved story, isolated environment, evaluation evidence and feature branch. Explicitly tell the tool to read `.ai/foundation/` and `.ai/project/` using the [bootstrap](04-use-agent-with-chat-ai.md#reusable-bootstrap-prompt). Ask for source/revision references before implementation. Merely creating `.ai/` does not activate an agent.

Configure permissions in the tool and repository, not only in a prompt. Start with read access; enable scoped feature-branch edits and verified safe local commands when needed. Optional tool-specific instruction files may point to the pinned documents, but should not copy or rewrite the global policies. Check their current loading rules and precedence in that tool's official documentation.

| Initially permitted within task scope | Initially excluded |
| --- | --- |
| Read approved repository files | Production access and production database writes |
| Modify feature-branch task files | Cloud administration and unnecessary secrets |
| Run verified safe local commands/tests | Destructive operations without required authorization |
| Inspect Git diff and test evidence | Direct push/merge to main/develop and automatic deployment |

Tests may reset databases or trigger external services. Verify effective targets and apply the [Laravel command gates](../agents/backend/stacks/laravel/commands.md) when using that profile; a command named “test” is not inherently safe. Broader permissions require the applicable governance, and production deployment remains prohibited for agents.

For Codex-specific permission setup, consult the [official security documentation](https://learn.chatgpt.com/docs/security). Product configuration is optional integration detail, not a new foundation policy or a guarantee that every mode enforces the same boundaries.

## Working sequence

```text
Approved story → Read .ai/ → Inspect repository → Plan
→ Human plan/action approval when required → Scoped implementation
→ Tests → Self-review → Independent Security review → Remediation/retest
→ PR and Audit evidence review → Human review
```

A PR is a review record, not a merge. A draft PR can be opened earlier under the approved workflow so Audit can verify its existence. Required Audit evidence must be available before the relevant human decision. Human approval of a plan does not authorize every sensitive command; avoid inventing a universal plan-approval requirement where policy does not require one.

Stop for missing context or required authorization, preserve unrelated work, and report actual commands/results. Never treat the tool's ability to perform an action as permission. See the [coding example](examples/coding-agent-example.md).
