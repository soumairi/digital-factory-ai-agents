# Git Policy

- Make changes on a dedicated working branch and submit them through the repository's review process.
- No agent may merge directly to `main`, push changes directly to `main`, or bypass branch protection. Integration into `main` requires an authorized human through protected repository controls.
- No agent may deploy to production.
- Keep commits and proposed changes focused, understandable, and traceable to the authorized task.
- Inspect the working tree before editing. Do not overwrite, discard, or revert unrelated work.
- Do not commit credentials, confidential project data, generated clutter, or unnecessary dependencies.
- Include a clear change description, relevant validation results, and known limitations in review submissions.
- Obtain explicit human approval before destructive Git operations, shared history rewrites, or changes to repository permissions and protection rules. Approval cannot waive the prohibitions above.
- Update the foundation version and changelog for released changes. Consumers adopt releases explicitly rather than silently tracking a moving branch.

## Further definition

- **TBD:** Release owner, release tagging process, and minimum reviewer requirements.
- **Project layer responsibility:** Define branch naming and concrete repository protection settings consistent with this policy.
