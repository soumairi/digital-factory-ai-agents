# Example: the same definition in a coding tool

Use an organization-approved repository-aware tool, such as Codex, Claude Code, Cursor or another compatible runtime. The project definition is the same as in chat mode; only available tools and evidence collection change.

```text
Repository
   ↓
.ai/foundation/ (pinned instructions)
   ↓
.ai/project/ (actual project context)
   ↓
Coding Agent (scoped permissions)
   ↓
Feature Branch → Tests → Self-review
   ↓
Independent Security Review → Fixes/reverification if needed
   ↓
Pull Request → Audit evidence review
   ↓
Human Review
```

A draft PR can be created earlier under the authorized workflow; the diagram shows handoff dependencies, not a rule that prevents early review records.

## Example task instruction

```text
Read .ai/foundation/shared/, the Backend README/core, the Laravel profile,
and all .ai/project/ files. Confirm the foundation and project revisions.
Use the Backend lifecycle and stage prompts. Inspect the repository before edits.

Approved story: [reference and acceptance criteria].
Working branch: [feature branch].
Allowed targets and commands: [approved project commands/context references].

First report understanding, missing information, assumptions, security risks
and a focused plan. Pause dependent work for missing context or approval.
Then implement only the authorized story, run verified safe tests, review the
diff and produce the core technical report. Do not modify the foundation snapshot.
Do not merge, deploy, access production or seek unnecessary secrets.
Prepare evidence for separately assigned Security and Audit reviewers.
```

The developer verifies that the tool actually reads the files and that OS/tool permissions restrict access to the intended workspace and test resources. Inspect the diff and executed commands; do not trust a “done” message without evidence. Tool-specific instruction loading is optional and must be checked against the installed tool's documentation.

For the [Customer Portal scenario](backend-laravel-agent-example.md), expect a narrow change to the existing request/authorization/query/serialization path and tests, not a new architecture or authentication package. If a command could reset data, apply the Laravel command gates before execution.

Use the [coding guide](../05-use-agent-with-coding-ai.md) and [Security/Audit handoff](../06-security-and-audit-workflow.md). No commands or actual agent runs are performed by this example.
