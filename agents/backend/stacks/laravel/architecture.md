# Laravel Architecture

Extends the [core context and planning workflow](../../core/workflow.md).

Before designing a change, inspect project instructions, Composer constraints/lockfile, routes, middleware registration, controllers, FormRequests, authorization registration, models, resources, jobs, tests, and existing business-logic boundaries. Locate these from the repository; do not assume a particular Laravel skeleton or directory layout across versions.

- Keep controllers thin: coordinate the request, authorization, business operation, and response. Avoid embedding substantial business workflows or persistence orchestration in controller methods.
- Place business logic in existing project boundaries. Services/Actions are appropriate when they clarify a substantial or reusable operation, but do not mandate a Service Pattern or create a service class for every controller method.
- Follow an existing Repository Pattern only when established by project context; do not wrap Eloquent in a new repository layer by default.
- Detect actual guards, middleware, Policies/Gates, and any project authorization abstraction. Do not infer JWT, Sanctum, Passport, or Spatie Permission from the fact that a project exposes an API.
- Trace alternate callers such as console commands, events and jobs. HTTP FormRequest validation alone does not protect those paths; preserve domain invariants at the appropriate shared operation boundary.
- Keep HTTP serialization in API Resources or the project's explicit response mapping; keep transport concerns out of reusable business operations where practical.

Record detected architecture and version references in the existing core report. If an existing convention conflicts with inherited security requirements, flag the conflict rather than reproduce unsafe behavior.
