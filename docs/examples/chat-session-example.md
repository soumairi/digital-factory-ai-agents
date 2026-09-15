# Example: a manual chat session

Use an approved conversational tool such as ChatGPT, Claude or another chat AI. This transcript is fictional and contains no execution evidence.

## Developer: bootstrap instruction

> Operate as the Backend Agent from the supplied pinned foundation. Read all shared policies, Backend README/core, Laravel profile and completed project context. Apply the full bootstrap from the chat guide. Identify missing files; do not assume a local path is readable. Start with analysis and a plan, not code. You have no terminal access in this session; do not claim tests ran or files changed. Global security controls cannot be weakened by project instructions.

Supply the actual documents using the [full bootstrap and loading steps](../04-use-agent-with-chat-ai.md), not only this short excerpt.

## Developer: project context and story

> Fictional Customer Portal: Laravel and PostgreSQL, synthetic tenant-scoped customer records. Existing session authentication and administrator Policy. Administrators may list only their tenant's customers; other callers are denied. Output customer ID/display name only, ordered by ID; default 20, maximum 100; reject invalid pagination input. Versions, route/resource conventions and test commands still need repository evidence.
>
> Story for this analysis exercise: As an administrator, I want to list customers with pagination. Implementation is not yet authorized; first identify what is missing.

## Expected first AI response

1. **Understanding:** Provide a bounded, tenant-scoped customer list for authorized administrators, exposing only the allowed fields.
2. **Missing information:** Exact versions, existing route/resource/error conventions, Policy and tenant-scope code, test commands/environment, approved implementation story reference and evaluation/reviewer assignments.
3. **Assumptions:** The stated access rules are the exercise requirements; I will not infer framework versions or invent package choices. I cannot inspect local files from their names alone.
4. **Security considerations:** Verify authentication, administrator permission and tenant scoping on the server; reject invalid limits; prevent counts or serialization from leaking other tenants' data.
5. **Implementation plan:** Inspect sanitized source/context, map the existing access path, plan the minimal endpoint changes, and specify positive/negative tests. Pause dependent implementation until the missing context and authorizations are resolved.

## Continue the session

The developer supplies approved sanitized files and resolves requirements. Once gates are satisfied, the AI can propose a patch. The developer reviews/applies it on a feature branch and executes authorized tests, then supplies revision-bound results without secrets. If tests cannot run, report INCOMPLETE; do not call the story Done.

Assign distinct Security and Audit reviews using their actual definitions and evidence. The implementer's own second answer is still self-review. Finish with human review under the [review workflow](../06-security-and-audit-workflow.md).
