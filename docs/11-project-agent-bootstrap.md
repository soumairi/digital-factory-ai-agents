# 11. Project agent bootstrap

## Purpose and prerequisites

`scripts/init-project-agent.sh` prepares an existing **local** project for Backend/Laravel work. It copies a minimal foundation bundle and the existing project templates. It does not run an agent, configure an AI tool, fetch a repository or synchronize with a remote.

Use Bash 3.2+ on Linux/macOS and standard Unix tools. No jq, Python, Node, PHP, Composer or Docker is required. Obtain a trusted foundation checkout first. The target must already exist and must not be `/` or inside the foundation source checkout. Use a local non-production workspace; the script cannot establish the business purpose of a mounted filesystem.

## Command syntax

From the foundation checkout:

```sh
./scripts/init-project-agent.sh --help
./scripts/init-project-agent.sh backend laravel ../customer-portal
./scripts/init-project-agent.sh backend laravel ../customer-portal --dry-run
```

From a project directory, invoke the script by its actual absolute or relative path and pass `.`. If the script is accessible at the illustrated relative path, these forms also work:

```sh
./scripts/init-project-agent.sh backend laravel . --dry-run
./scripts/init-project-agent.sh backend laravel . --force
```

Here `.` always means the caller's directory, not the foundation repository. Running those literal commands from the foundation root is deliberately rejected. For the usual separate checkouts, use `/path/to/digital-factory-ai-agents/scripts/init-project-agent.sh backend laravel .` from the project. Quote paths containing spaces. Only backend/laravel is supported; there is no fallback.

## Fresh installation and dry-run

A fresh run requires `.ai/` to be absent. Preflight verifies required source files and destination types before writing. `--dry-run` uses the same validation and lists the target, version, directories, copies and preserved files without writing even temporary files. Existing `.ai/` requires `--force`, including for a refresh preview.

## Installed directory structure

```text
.ai/
├── README.md
├── agent-manifest.json
├── foundation/
│   ├── README.md
│   ├── VERSION
│   ├── shared/                  # all seven shared policies
│   ├── backend/
│   │   ├── README.md
│   │   ├── core/                # six core documents
│   │   ├── prompts/             # five referenced lifecycle prompts
│   │   └── laravel/             # eight profile documents
│   ├── security/                # six role documents
│   └── audit/                   # seven role documents
└── project/
    ├── README.md
    ├── project-context.md
    ├── tech-stack.md
    ├── architecture.md
    ├── coding-conventions.md
    ├── commands.md
    ├── security-context.md
    ├── compliance-context.md
    ├── definition-of-done.md
    └── agent-overrides.md
```

This is a compact bundle, unlike the full snapshot in the older [manual guide](03-create-project-agent.md). Backend README/prompts are included because the core/profile references depend on them. Relative Markdown links are adapted to the compact paths without changing rules. A generated foundation index supplies the shared-policy map. No unrelated agents, application files or evaluations are copied.

## Foundation versus project layer

The manifest records Backend, Laravel and included Security/Audit roles. `.ai/foundation/VERSION` is the sole authoritative installed version. No project-layer version file is generated. Existing project-layer `FOUNDATION_VERSION` files remain untouched as legacy content, not installed-version authority or approval state. These scripts do not certify review, publish a tag or configure a runtime.

Do not customize `.ai/foundation/` for project needs. Complete `.ai/project/` using actual evidence; database, authentication, authorization libraries, architecture, cloud and domain remain placeholders. Read the generated `.ai/README.md` for the actual load paths. References to central repository structure inside copied explanatory prose still describe the source repository, not additional installed files.

## Force refresh and foundation updates

`--force` refreshes managed foundation files and generated README/manifest files. **Every existing file under `.ai/project/` is preserved byte-for-byte**, including README and any legacy FOUNDATION_VERSION; missing template files are added. Unrecognized/stale files are not deleted anywhere. Force is an explicit local copy operation, not remote synchronization or automatic adoption.

Review the source changelog/diff and back up project work before refreshing. Preview with `--force --dry-run`. Then check foundation/VERSION, evaluate the updated rules and resolve conflicts/exceptions through team review. Record the immutable source revision manually in project context; the script never runs Git. Do not assume preserved project context is compatible with a new version.

## Security behavior

The script reads an explicit inventory of foundation documents and templates. It never reads application `.env` files, searches for credentials, runs project code, calls AI APIs or invokes Git, Composer, Artisan, migrations or deployment commands. It performs only local filesystem operations. No network access or production authority is granted.

Symbolic source components and symbolic/special nodes anywhere under existing `.ai/` are rejected. Existing files are replaced using a temporary file and rename so external hard-linked contents are not overwritten in place. Required-source and destination-type failures happen before writes. Do not run concurrently with another initializer or process modifying `.ai/`; v0.1 assumes a trusted, quiescent local workspace and does not prevent hostile filesystem races.

## Troubleshooting and limitations

- **Already exists:** inspect `.ai/`, then use `--force --dry-run`; never delete project context to get past the check.
- **Unsupported combination:** only backend/laravel is implemented.
- **Missing source:** restore the reported file in the trusted checkout; no target files are created for this preflight failure.
- **Symbolic link/type conflict:** use ordinary files/directories in a safe workspace; do not bypass checks by broadening permissions.
- **Permission or disk failure during writes:** the error identifies the target and possible temporary file. Inspect the partial installation before retrying. Per-file replacement is used, but the whole installation is not transactional and does not roll back completed writes.
- **Version format:** v0.1 accepts numeric `major.minor.patch`; prerelease/build suffixes are not supported.
- **New source documents:** the explicit source inventory must be updated deliberately when dependencies are added; arbitrary newly added files are not copied automatically.

Validate with `bash tests/scripts/test-init-project-agent.sh`. Tests use temporary fixtures, never real projects. Linux/macOS are the intended platforms; validate on your own OS before adoption.

After initialization complete context, permissions and review assignments, prepare isolated fixtures and run the [evaluation protocol](../evals/backend/README.md) from the central repository. Then follow [coding mode](05-use-agent-with-coding-ai.md) or [chat mode](04-use-agent-with-chat-ai.md), substituting compact paths. No orchestration or runtime integration is installed.

For existing installations, prefer the [Foundation updater](12-update-project-foundation.md), which adds whole-Foundation staging, backups, integrity checks and rollback while preserving the entire project layer. New bootstraps generate `foundation/checksums.sha256` when `sha256sum` or `shasum` is available. The older bootstrap `--force` behavior described above remains compatible, but does not provide the updater's recovery guarantees.
