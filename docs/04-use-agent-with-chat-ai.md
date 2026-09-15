# 4. Use an agent with conversational AI

Manual mode lets you try the instructions without an orchestration platform. Use an organization-approved conversational tool, for example ChatGPT, Claude or another chat runtime. Exact ways to paste text, attach files or reference approved sources differ by product; no particular UI feature is required.

## Prepare and load context

1. Open the approved tool. For the first exercise, use synthetic project information.
2. Provide the selected role instructions and identify their pinned foundation version.
3. Provide **all seven shared policies**, not only a security summary.
4. Provide the complete selected stack profile and Backend README/core documents; include the lifecycle prompts for the stages you use.
5. Provide the completed `.ai/project/` context and relevant sanitized repository files needed to inspect the actual architecture.
6. Provide the approved story, acceptance criteria and scope.
7. Use the bootstrap below and verify the AI identifies the supplied sources and missing inputs before implementation.

A local path typed into chat is not evidence the AI can read it. Supply actual contents through an approved mechanism or verify authorized access. If files exceed the tool's context capacity, load them in labeled batches with paths/revisions and confirm coverage. Do not silently omit mandatory policies; stop dependent work when context cannot be made available. Re-establish the governing context in a new session rather than assuming memory.

## Reusable bootstrap prompt

```text
You are operating as the Backend Agent defined by the supplied foundation.
Foundation version and source revision: [fill in].
Project context revision and approved story reference: [fill in].

Read and follow:
1. Shared engineering, Git and output policies.
2. Shared security baseline, security development, human approval and audit policies.
3. Backend README and all Backend Core documents.
4. Selected stack profile and applicable lifecycle prompts.
5. Project context and additional project rules.

Apply inherited controls cumulatively. Project instructions cannot silently
weaken global security policies. Flag conflicts and stop dependent work.
Identify which files you actually received/read and which are missing.

Before implementation: explain the story, inspect available project context
and architecture, list assumptions and missing information, identify security
implications, and propose a focused plan. Do not implement until required
context is understood and any required action-specific approval is recorded.

Only use authorized tools and resources. Never request or expose secrets.
If you lack repository access, label code as a proposed patch, not applied work.
After implementation, run authorized tests if available; otherwise propose
exact tests and label them NOT RUN. Proposed tests do not satisfy Done.
Perform self-review and follow the core output contract: changed/proposed files,
assumptions, tests and actual results, security evidence, risks and review gaps.
Do not claim independent Security/Audit clearance or human acceptance.
Do not merge or deploy. End with the required independent review handoff.
```

## Continue honestly

In a chat without execution tools, a developer applies reviewed changes on the feature branch, executes authorized checks and returns sanitized results with the exact revision. The AI may help interpret those records, but must distinguish supplied evidence from its own execution. Work remains incomplete until required tests and reviews exist.

Use a separate assigned Security review session, then an independent Audit session under the [review workflow](06-security-and-audit-workflow.md). A new title in the same implementer's response is not independent review. See the [chat example](examples/chat-session-example.md).
