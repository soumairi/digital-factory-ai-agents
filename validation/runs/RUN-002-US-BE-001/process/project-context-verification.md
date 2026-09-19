# Project context verification

Run ID: RUN-002-US-BE-001. Recorded UTC: 2026-09-19T13:14:14.913518+00:00. New prospective record; prior evidence unchanged.
Sandbox-relative paths below refer to `/private/tmp/digital-factory-run002-zct1ohhz/app`.

| Item | Verified Value | Evidence |
|---|---|---|
| Project | Customer Portal Sandbox — RUN-002 | .ai/project/project-context.md |
| Purpose | Backend Agent validation only | Current user instruction; .ai/project/project-context.md |
| Sandbox | `/private/tmp/digital-factory-run002-zct1ohhz/app`; newly extracted upstream scaffold | sandbox-baseline.txt |
| Backend | Laravel 13.24.0 | composer.lock; sandbox-effective-configuration.json |
| PHP | 8.3.33; explicit /opt/homebrew/opt/php@8.3/bin/php -n | sandbox-effective-configuration.json; preflight/run.py |
| Database | SQLite :memory:, empty, no backing file | sandbox-effective-configuration.json: PRAGMA database_list and tables |
| Authentication | Existing web/session guard and Eloquent users provider; customer endpoint authentication NOT YET IMPLEMENTED | config/auth.php; effective configuration; sandbox-routes.json |
| Authorization | Customer access NOT YET IMPLEMENTED; standard Laravel Gate/Policy planned under the profile | Empty AppServiceProvider; .ai/project/architecture.md |
| Architecture | bootstrap/app.php routing; app/Models/User; app/Providers; welcome and health routes; no customer domain/API endpoint | Bootstrap, app and routes inspection; sandbox-routes.json |
| Testing | PHPUnit 12.5.33; two stock tests discovered, not executed | composer.lock; sandbox-test-discovery.txt; tests/TestCase.php and ExampleTest files |
| Safe local commands | python3 preflight/run.py inspect, test-list, routes; test and format-check reserved for later phase and reinspection of changed hooks/tests | .ai/project/commands.md; wrapper source; test discovery |
| Production | NONE | New local scaffold; no remote or production configuration imported |
| Sensitive Data | NONE — synthetic data only | New empty DB; no .env imported or real fixtures loaded |
| Working branch | validation/run-002-us-be-001 | sandbox-baseline.txt |
| Baseline | Pristine acbfa28f05ec7aac81fc4597c0930833dda00e49; setup 256b048234e6b40e06a2fff70d2e15c884ed482e; clean tree | sandbox-baseline.txt |
| Applicable instructions | Installed .ai/foundation and populated .ai/project; additional inventory recorded | sandbox-instruction-inventory.md |
| US-BE-001 | NOT YET IMPLEMENTED | Application source unchanged from pristine scaffold |

Current observations replace historical assumptions prospectively. This is environment preparation, not an implementation or security assessment. Unknown endpoint features are explicitly unimplemented, which is expected before implementation and does not imply missing sandbox context.
