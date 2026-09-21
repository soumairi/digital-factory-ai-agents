# Laravel Database Rules

Specializes the data-integrity, injection, mass-assignment and resource-limit requirements in the [core Definition of Done](../core/definition-of-done.md).

## Assignment and relationships

- Use an explicit `$fillable` / `$guarded` strategy consistent with project conventions. Review each changed model's writable fields; never disable guarding globally to make a request succeed.
- If the existing project uses `$guarded = []`, require an explicit trusted field mapping at every affected write boundary. Never send arbitrary request arrays to `create`, `update`, `fill`, or equivalent writes. Model guarding is not protection for raw/query-builder writes.
- Assign owner, tenant, role and other protected fields from trusted authorized context, not caller-supplied ownership claims. Validated foreign-key existence is not authorization to associate that object.
- Verify related objects belong to the authorized scope before `attach`, `sync`, reassignment, nested writes or relationship traversal. Scope relationship queries and route bindings appropriately; neither binding nor a global scope alone proves operation permission.

## Queries and performance

- Use parameterized Eloquent/ORM or query-builder operations for untrusted values. Bind values in necessary raw expressions; never concatenate request input into SQL.
- Allowlist client-selectable columns, sort directions and operators: value bindings do not protect dynamic SQL identifiers.
- Prevent N+1 queries by inspecting relationship access in loops and serialization. Use constrained eager loading where appropriate and load only authorized, needed relations/columns. Consider version-supported lazy-loading detection in development/tests when consistent with project tooling.
- Preserve owner/tenant constraints in eager loads, aggregates and list queries. Pagination belongs in [API rules](api-rules.md); it does not replace access scoping.

## Integrity and migrations

- Use `DB::transaction` or the established transaction boundary for multi-step critical writes that must succeed or fail together. Verify rollback and concurrency behavior; use constraints and locking where the business invariant requires them.
- Do not assume a database transaction rolls back files, external calls or messages. Coordinate those effects deliberately, and dispatch relevant queued work after commit using supported project mechanisms.
- Treat mass updates/deletes carefully: do not rely on per-model events being executed for bulk query operations. Preserve required authorization, invariants and audit evidence explicitly.
- Review migrations for data loss, locks, indexes, foreign keys, defaults and reversibility. Follow project migration history conventions; do not edit an already applied migration to disguise a new change.
- Execution authorization, including destructive reset commands and test-triggered resets, is defined solely in [commands](commands.md).

Framework references: [Eloquent mass assignment](https://laravel.com/framework/docs/10.x/eloquent), [database transactions](https://laravel.com/framework/docs/12.x/database), and [migrations](https://laravel.com/framework/docs/12.x/migrations). Use the consuming project's version for API details.
