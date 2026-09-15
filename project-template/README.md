# Project Integration Template

Copy this directory into a consuming repository, for example `.ai/project/`, and fill its placeholders there. These files are reusable blank templates; real project details and lessons containing confidential information never belong in the global repository.

## Separation and composition

GLOBAL FOUNDATION: the immutable pinned release containing shared policies, agent cores, stack profiles, and evaluation specifications.

PROJECT-SPECIFIC CONTEXT: this copied template, completed with one project's requirements, conventions, commands, access boundaries, and additional constraints.

Global Foundation + Agent Core + Stack Profile + Project Context = Project-Specific Agent.

Project rules ADD constraints or supply context. They cannot silently replace global rules. See `agent-overrides.md` for conflict and exception handling; a request does not grant an exception.

## Manual integration

1. Obtain an approved foundation release as a read-only checkout or versioned snapshot outside application source. Keep the selected release intact; do not modify it to customize a project.
2. Copy this template to the project. Set `FOUNDATION_VERSION` to the exact adopted foundation version and record the source and immutable commit/digest in `project-context.md`. The shipped value identifies the release containing this template; it does not prove that release has been published or approved.
3. Fill all context documents using actual repository evidence. Mark non-applicable fields with reasons; unresolved `TBD` items block dependent work.
4. Select Backend Core and, for Laravel projects, the Laravel profile. Follow their README links to load all required documents and shared policies. Resolve those links within the foundation checkout, not the copied template directory.
5. Assign separate implementation, Security and Audit reviewers and human approval authorities. Configure an isolated test environment and enforce least privilege in the chosen tool before execution.
6. Provide the pinned documents and project context to the chosen runtime manually. No automatic prompt loader, permissions integration, or executable agent is provided here.
7. Run the applicable foundation evaluations before a real story. Keep results and context revisions in the consuming project's approved evidence location.

## Files to complete

| File | Project-owned content |
| --- | --- |
| project-context.md | Scope, owners, source/revision and story references |
| tech-stack.md | Verified versions, dependencies and selected profile |
| architecture.md | Actual boundaries, flows and decisions |
| coding-conventions.md | Evidenced naming/style and added constraints |
| commands.md | Exact approved commands, targets and side effects |
| security-context.md | Access matrix, data boundaries and security decisions |
| compliance-context.md | Applicable policies, authorities and evidence handling |
| definition-of-done.md | Additional project acceptance and evidence gates |
| agent-overrides.md | Additive rules, conflicts and exception requests |
| FOUNDATION_VERSION | Exact pinned foundation version |

## Adoption of updates

Review the candidate changelog/diff, compare local additions and exceptions, run relevant evaluations and project regressions against the candidate, and obtain human adoption approval. Update the foundation artifact, version pin and immutable source reference together in a project PR. Preserve prior results and the previous pin for rollback; do not auto-track a moving branch. Template updates are reviewed field by field, never copied over completed project context blindly.
