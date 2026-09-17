# 3. Create a project-specific agent

This guide uses `.ai/foundation/` for a pinned foundation snapshot and `.ai/project/` for your own context. These are proposed project paths, not folders automatically discovered by every AI tool.

1. **Create or clone the software project.** Inspect its current branch and preserve unrelated work. Work on a feature branch under project Git policy.
2. **Add the foundation at `.ai/foundation/`.** Obtain the approved repository URL and approved release/commit from your maintainer. Clone or copy an intact versioned snapshot there, outside application source directories. Treat it as read-only; keep its source and immutable revision. A separate checkout is also valid if you consistently adjust paths. Never assume a tag exists just because VERSION contains a number.
3. **Copy the complete [project template](../project-template/README.md) to `.ai/project/`.** Do not alter the global template with your real project details.
4. **Select a core.** For backend work, use `agents/backend/core/` plus its README and lifecycle prompts from the snapshot.
5. **Select a profile.** For Laravel, add `agents/backend/stacks/laravel/`. Django, FastAPI and Node currently contain placeholders, not implemented profiles.
6. **Complete project context.** Inspect actual versions, architecture, commands, access rules and owners. Read the installed version from `.ai/foundation/VERSION` and record the source commit/digest in project-context.md; do not create a second installed-version record. Fill every required field or explain non-applicability; unresolved facts block dependent work. Assign independent Security/Audit reviewers and human approval owners.
7. **Run initial evaluation.** Prepare isolated synthetic fixtures and runnable assertions for the [backend cases](../evals/backend/README.md). Follow their evidence and scoring protocol; all nine cases are needed for initial suite readiness. These files are specifications, not a ready-to-run harness. If setup is incomplete, restrict the first conversation to analysis and record the gap.
8. **Start a small approved User Story.** Supply acceptance criteria and approval reference, then use [chat mode](04-use-agent-with-chat-ai.md) or [coding mode](05-use-agent-with-coding-ai.md).

## Resulting project structure

```text
my-project/
├── app/
├── tests/
└── .ai/
    ├── foundation/          # intact pinned foundation contents
    └── project/
        ├── README.md
        ├── project-context.md
        ├── architecture.md
        ├── tech-stack.md
        ├── coding-conventions.md
        ├── commands.md
        ├── security-context.md
        ├── compliance-context.md
        ├── definition-of-done.md
        ├── agent-overrides.md
        └── FOUNDATION_VERSION  # legacy template reference only, omitted by bootstrap
```

The canonical filename is **project-context.md**. Some informal examples call this `context.md`; this guide uses the existing template name throughout so no renaming or duplicate source of truth is needed.

Keep the foundation snapshot unchanged. Project additions belong in `.ai/project/`; secrets belong only in approved organizational secret-management mechanisms. Do not copy production credentials, passwords, tokens or private keys into these files or conversational tools. Share other sensitive context only through approved organizational channels and data policies.
