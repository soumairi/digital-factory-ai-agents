# Laravel API Rules

Specializes core API safety without changing the project's established contract.

- Follow existing route prefixes, versioning, middleware groups, naming and status/error conventions. Inspect registered routes and their authorization path rather than assuming an API middleware group protects every endpoint.
- Apply [FormRequest rules](coding-rules.md) for incoming schemas and [security rules](security-rules.md) before protected operations. Binding a model by ID is not authorization.
- Use API Resources or an explicit allowlisted safe serialization mapping. Do not expose arbitrary model attributes or loaded relationships by returning models without reviewing output fields.
- Review nested resources, conditional fields and computed attributes for sensitive data and access boundaries. `$hidden` is supplemental protection, not a substitute for an explicit response contract.
- Where API Resources are used, use version-supported conditional relationship inclusion, such as `whenLoaded`, to avoid hidden relationship queries; plan required eager loads under [database rules](database-rules.md).
- Paginate list endpoints using the existing paginator/response convention. Validate page/cursor inputs and bound client page sizes. Apply access scopes before pagination and counts, and use a stable ordering appropriate to the pagination method.
- Preserve documented error semantics through Laravel's configured exception handler. Avoid exposing exception messages, stack traces, SQL, configuration or internal paths. Test the project's intended forbidden/not-found behavior without disclosing object existence unnecessarily.
- Use the project's rate-limiter and CORS configuration where applicable; do not invent limits or broaden origins without requirements. These mechanisms do not substitute for authorization.

Framework reference: [Laravel API Resources](https://github.com/laravel/docs/blob/13.x/eloquent-resources.md). Verify availability and behavior against the project's version.
