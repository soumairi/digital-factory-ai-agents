# Laravel Security Rules

Specializes the [core security Done gate](../../core/definition-of-done.md) and inherits the [shared security gate](../../../../shared/security-development-policy.md#security-gate-and-finding-governance). The full core checklist still applies; this document describes Laravel implementation mechanisms only.

## Authorization

- Use Policies/Gates or the existing project authorization conventions, with the actual configured guard and middleware. Authentication alone is insufficient.
- Authorize before sensitive object data is disclosed or modified. Resolve only the object/context needed for the authorization decision within appropriate access scopes; do not eagerly expose related sensitive data first.
- Check the specific action and owner/tenant relationship, including nested endpoints, bulk operations, relationship mutation and jobs. Scoped route-model binding helps constrain lookup but does not replace operation authorization.
- Apply FormRequest authorization as described in [coding rules](coding-rules.md). Do not assume installed authentication/permission packages are active or correctly configured for the route.

## Uploads and storage

- Use version-supported file validation for permitted content/type and size. Do not trust client extensions, MIME labels, names or paths alone; include project-required scanning or processing restrictions.
- Store sensitive uploads on an approved private disk with safe generated names and least-privilege access. Do not publish them through a public disk or storage link by default.
- Authorize downloads and any temporary access links according to project requirements. Handle failed persistence/storage steps without orphaning sensitive data or weakening access controls.

## Queues and jobs

- Inspect queue connection, worker privileges, serialized payloads and failed-job storage. Minimize sensitive payloads; do not serialize passwords or bearer tokens as convenient job context.
- Preserve explicit actor/tenant context and validate the job's authority at execution under defined business rules, particularly when permissions or ownership can change while queued.
- Design bounded retries/timeouts and idempotency for replayed work. Follow [database rules](database-rules.md) for after-commit dispatch; never assume queue execution inherits request-time authorization or an open transaction.
- Use only isolated queues during testing. Do not run workers against shared queues as a routine verification step.

## Configuration and logs

- Require production-suitable Laravel configuration: `APP_DEBUG=false` and effective `config('app.debug')` false, protected application keys, restricted filesystem access, intended HTTPS/session settings, and no exposed debug tooling. Setting `APP_ENV=production` alone is insufficient.
- Supply secrets through approved environment/secret management. Keep `env()` reads in configuration files and consume values with `config()` in application code so configuration caching is respected. Do not commit `.env` secrets or dump configuration into reports.
- Verify intended and cached/effective settings through approved sanitized evidence; this profile grants no production access or deployment permission.
- Use secure logging with redaction. Never log tokens or passwords; avoid complete requests, authorization headers, connection strings and sensitive job payloads. Review both application and exception/failed-job logs.
- Use the project's configured credential hashing/authentication facilities when relevant; do not invent a token scheme or assume JWT, Sanctum or Passport.

Framework references: [authorization](https://laravel.com/framework/docs/12.x/authorization), [file storage](https://laravel.com/framework/docs/12.x/filesystem), [queues](https://laravel.com/framework/docs/12.x/queues), [configuration](https://laravel.com/framework/docs/9.x/configuration), and [deployment configuration](https://laravel.com/framework/docs/master/deployment). Match APIs to the installed version; these references grant no execution authority.
