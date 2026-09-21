# Laravel Testing Rules

Extends the [core automated negative-test gate](../core/definition-of-done.md#automated-negative-test-gate), without replacing its six categories or evidence requirements.

- Discover the project's Laravel/PHP versions, PHPUnit/Pest setup, test conventions, database configuration, and Composer/Artisan wrappers. Do not install a test framework or authentication package by assumption.
- Add automated feature tests for changed routes, middleware, authorization, request validation, serialization and persistence. Add unit tests for isolated business rules where appropriate; unit tests alone do not verify HTTP access controls.
- Use the real configured guard and authorization path in feature tests. Use supported authentication helpers where appropriate, but test actual credential failures where the story requires them. Do not disable authorization middleware to make negative tests pass.
- Include negative authorization and ownership boundary tests: another user/tenant, insufficient role, substituted route IDs, related-object IDs and protected-field manipulation. Assert the intended response, absence of sensitive fields, and absence of unauthorized database changes.
- Exercise FormRequest invalid/malicious payloads and explicit output schemas. Use framework database assertions to verify protected fields remain unchanged.
- Test transaction failure behavior, relevant concurrent invariants, bounded pagination and N+1-sensitive paths with representative fixtures. Avoid brittle query counts that do not measure an actual performance requirement.
- Where relevant, use supported storage/upload and queue fakes to avoid external side effects. A queue fake proves dispatch assertions, not job execution safety; separately test the handler, access checks and retry/idempotency behavior.
- Before using database reset traits, migrations, factories or parallel tests, apply the sandbox and authorization gates in [commands](commands.md). A `.env.testing` filename or a test command is not proof that resources are disposable.
- Record commands, revision, results, skipped checks and Laravel-specific evidence using the existing [core output contract](../core/output-contract.md). Preserve independent Security and Audit handoffs.

Framework reference: [Laravel testing](https://laravel.com/framework/docs/12.x/testing). Use version-matched HTTP, database and mocking documentation for concrete APIs.
