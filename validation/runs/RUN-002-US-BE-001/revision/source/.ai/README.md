# Project AI Agent Foundation

This project uses the Digital Factory AI Agent Foundation.

Backend Agent Core + Laravel Stack Profile + Global Engineering & Security Policies
+ Project Context = Project Laravel Backend Agent.

- [foundation/README.md](foundation/README.md) indexes versioned global rules.
- [project/project-context.md](project/project-context.md) starts project-specific context and constraints.
- foundation/VERSION is the authoritative installed version.
- agent-manifest.json records only the selected Backend/Laravel configuration.

Do not customize files under .ai/foundation/ for project-specific needs. Project
configuration belongs under .ai/project/. Contribute reusable improvements back
to the central digital-factory-ai-agents repository.

This compact installation uses foundation/backend/core/ and foundation/backend/laravel/;
it is not a full repository snapshot. Read backend/README.md and its linked prompts,
all shared policies, the profile and completed project context. Load Security and
Audit definitions separately for independent review. No AI tool is configured automatically.

The foundation does not authorize production access, merges or deployments.
Global controls remain mandatory; project additions cannot silently weaken them.
Never place secrets in these files or conversational tools. Complete placeholders
without guessing database, authentication, cloud or business architecture.

A force refresh preserves every existing project file, including legacy FOUNDATION_VERSION
files. Those project-owned values are not consulted as installed-version metadata or
approval state. Read foundation/VERSION for the installed version.
Record the approved source revision in project context. Run required evaluations
using the central repository's evals/backend specifications and isolated fixtures;
those evaluation specifications are not copied by this minimal installer.
