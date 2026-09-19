# Laravel Coding Rules

Extends [core engineering responsibilities](../core/responsibilities.md); architectural placement is defined in [architecture](architecture.md).

- Use FormRequest classes for structured HTTP input validation. Define explicit server-side rules for types, sizes, formats, ranges, allowed nested keys, and project-required rejection of unexpected fields. Do not assume ordinary validation automatically rejects every unknown field.
- Pass a deliberately selected validated payload, using version-supported `validated()` or `safe()` APIs, to the operation. Do not pass `$request->all()` into persistence or treat validation as permission to write every accepted field.
- Keep FormRequest authorization deliberate: delegate to the Policy/Gate or established authorization boundary described in [security rules](security-rules.md). Returning `true` is appropriate only when authorization is enforced elsewhere or public access is explicitly required; document that boundary.
- Keep cross-entry-point invariants in the existing business operation, not only in a FormRequest or controller.
- Follow established naming, types, dependency injection, formatting and error conventions supported by the project's PHP/Laravel versions. Do not add a formatter or abstraction merely because this profile exists.
- Use the project's exception handling and error mapping; API-specific behavior is owned by [API rules](api-rules.md). Avoid catch-all handlers that conceal failures or return success after a failed operation.
- Follow [database rules](database-rules.md) for writable fields and query safety rather than assuming validated input alone prevents mass assignment.

Framework reference: [Laravel FormRequest validation](https://laravel.com/framework/docs/validation). Resolve the matching project-version documentation before implementation.
