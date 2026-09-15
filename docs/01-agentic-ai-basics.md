# 1. Agentic AI basics

An **agent definition** in this repository is a reusable set of written instructions, not a specific AI model. It describes a role, mission, engineering and security rules, workflow, guardrails (limits on actions), and expected outputs. Stack rules and project context complete the definition for one project.

An **AI runtime** is the tool or system that reads these instructions and produces responses or takes authorized actions. ChatGPT, Codex, Claude, Claude Code, Cursor, OpenAI-compatible agent runtimes and future AI systems are possible examples, not architectural dependencies. Their capabilities and permissions differ; compatibility must be evaluated, not assumed.

```text
Agent Definition + Project Context + AI Runtime
                    = Running Project Agent
```

Here, Agent Definition includes the selected shared rules, core and stack profile; Project Context supplies the local facts and additional constraints. Changing runtime does not change those rules, but does require rechecking permissions and evaluation results.

## Three ways to work

```text
Traditional AI:
Question → Answer

AI-assisted development:
Developer → Prompt → AI-generated code → Developer applies and verifies code

Agentic development:
Goal → Read context → Plan → Use authorized tools → Implement
     → Test → Self-review → Independent reviews → Human approval
```

You do **not** need to install a product called “Agentic AI.” You need an organization-approved runtime, the agent instructions and project context. Repository access, terminal access, test runners and other tools are optional for a first conversation; they are needed to execute and verify work directly. An orchestration framework schedules or coordinates automated work; none is required for manual use and none is implemented here.

Markdown describes intended behavior. It does not itself restrict tool permissions, run tests or guarantee compliance. A chat without tools can propose a patch and tests; it cannot truthfully claim to have changed local files or run those tests.

Start with [the architecture](02-foundation-architecture.md) or the [quick start](quick-start.md).
