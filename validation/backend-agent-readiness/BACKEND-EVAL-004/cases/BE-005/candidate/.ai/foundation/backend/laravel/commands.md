# Laravel Command Examples and Execution Gates

These examples are documentation, not instructions to run them in this foundation repository. Use only commands supported by the consuming project's versions and execution environment. Inspect Composer scripts, plugins, Artisan command behavior and application boot hooks before execution; apparently informational commands may boot project code.

Inherited [core guardrails](../core/guardrails.md) and [human approval policy](../../shared/human-approval-policy.md) remain authoritative. This file owns the Laravel-specific command classification; other profile documents reference it.

## Typical examples

| Example | Purpose | Conditions before execution |
| --- | --- | --- |
| `composer install` | Install project dependencies, normally from the committed lockfile. | Inspect scripts/plugins and allowed package sources; verify local write/network scope. If no lockfile exists, report that reproducibility is unresolved rather than silently treating dependency resolution as a locked install. Installation may execute code; inherited approvals apply to sensitive script effects. |
| `php artisan test` | Run automated tests. | Inspect test bootstrap, traits and connections; verify isolated database, cache, storage, queue, mail and outbound service configuration. If tests perform destructive resets, obtain explicit human authorization covering those resets before running. |
| `php artisan route:list` | Inspect registered routes. | Verify authorized environment and boot hooks; avoid exposing sensitive route metadata outside the review scope. This lists routes, not proof of effective authorization. |
| `php artisan migrate:status` | Inspect migration state. | Verify the actual resolved database target and read access before connecting. This is not permission to migrate. |

## Potentially destructive or sensitive operations

Explicit human authorization is required before potentially destructive commands or equivalent code paths, including migrations that drop/alter data, rollback/reset/refresh operations, seeding that overwrites data, queue clearing/retries with side effects, or destructive test setup. Shared-environment migrations and operational configuration/cache changes also require the approvals prescribed by shared policy. Flags such as `--force` do not provide approval or prove safety.

**`php artisan migrate:fresh` and `php artisan db:wipe` are blocked unless both explicit human authorization and sandbox verification are recorded.** Apply the same gate when invoked indirectly by a script, test trait or wrapper. Do not suggest them as automatic fixes for test failures.

For a permitted sandbox destructive action, verify and record before execution:

1. Exact command, working directory, code revision, purpose, and all affected connections/resources, including explicit connection flags, URL-based configuration and cached configuration. Avoid printing secret values.
2. The effective target is an isolated, disposable non-production sandbox, not merely named `local` or `testing`. Confirm isolation from shared databases, queues, disks and external services.
3. The data may be destroyed under the authorization; identify the recovery/recreation approach and expected impact.
4. An authorized human explicitly approved this command/effect on this target under the shared approval policy. Changed targets/effects require renewed authorization.

If any check is uncertain, do not execute. Verification itself must stay within existing access authorization.

## Production boundary

Destructive production commands are outside this Backend Agent profile and must not be executed by the agent. Escalate any such request to the separate human-controlled governance process; that process must require explicit human authorization and prior sandbox verification. Sandbox rehearsal does not authorize execution against production. The inherited prohibition on agent production deployment cannot be waived, and production access still requires separate governance authorization.

No command examples in this file grant merge, deployment, production access or permission to bypass approval gates.

Framework reference: [Laravel migrations](https://laravel.com/framework/docs/12.x/migrations), including the destructive semantics of fresh migration operations. Inspect concrete command behavior in the project's version before use.
