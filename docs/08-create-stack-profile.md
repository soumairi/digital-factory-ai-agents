# 8. Create a stack profile

A stack profile explains how a core requirement is implemented in a technology. It inherits the core; it does not create a new mission or replace security policy.

Potential locations include `agents/backend/stacks/django/`, `agents/backend/stacks/fastapi/` and `agents/backend/stacks/node/`. Their current README placeholders are not implementation guidance. [Laravel](../agents/backend/stacks/laravel/README.md) is the existing profile to inspect for structure.

1. Identify a real reusable need and the core being extended.
2. Inspect the target framework's official version-matched documentation. Require consuming projects to detect actual versions and conventions rather than assume packages or patterns.
3. Write a README explaining inheritance and files for needed architecture, coding, security, testing, database, API and command guidance. Avoid empty extra documents with no purpose.
4. Include only technology-specific mechanisms. Link generic lifecycle, Done and reporting rules back to the core.
5. Classify command side effects and inherited approval requirements. Do not introduce destructive shortcuts or production permissions.
6. Adapt foundation evaluation fixtures to the stack, verify security/regression outcomes, and submit a reviewed foundation PR.

| Layer | Illustrative wording |
| --- | --- |
| Backend Core | Validate input on the server. |
| Existing Laravel profile | Use FormRequest classes for structured HTTP validation; follow its full coding rules. |
| Possible Django profile | Use serializers/forms or the project's established validation mechanism, after verifying the actual stack and API framework. |

The Django row illustrates how to specialize wording; it is not a newly adopted policy or a claim that every Django project uses serializers. Likewise, do not relax Laravel's current FormRequest rule by paraphrasing it as an unrestricted alternative.

Check for duplication by asking whether each rule would be equally true in another framework. If so, reference the core/shared rule; keep only the stack-specific implementation detail. Single-project conventions belong in project context.
