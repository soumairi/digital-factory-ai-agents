# 12. Updating a project Foundation

Foundation updates refresh global engineering rules, security requirements, agent workflows, Definition of Done and stack guidance. Each project team reviews changes and explicitly runs the update. There is no background update, remote synchronization or automatic fleet update.

Global Foundation + Project Context = Project Agent. The updater replaces `.ai/foundation/`. It also removes an obsolete `foundation_version` field from a legacy manifest when replacement succeeds. **`.ai/project/` is NEVER replaced or edited, even with `--force`.** The existing `.ai/README.md` is preserved.

## Commands and prerequisites

Use a trusted local Foundation checkout, Bash 3.2+ and standard Unix utilities on macOS/Linux, including `awk` and a SHA-256 utility (`sha256sum` or `shasum`). Neither initialization nor updating requires Python, Node.js, PHP, Composer or jq. Python is used only by the repository's internal update test harness, for fixture creation, independent byte comparisons and fault injection.

```sh
# First initialization only
./scripts/init-project-agent.sh backend laravel ../customer-portal

# Review before updating
./scripts/update-project-foundation.sh ../customer-portal --dry-run
./scripts/update-project-foundation.sh ../customer-portal

./scripts/update-project-foundation.sh --help
./scripts/update-project-foundation.sh '../project with spaces' --force
```

Options can precede or follow the target. From the project directory, invoke `/path/to/digital-factory-ai-agents/scripts/update-project-foundation.sh . --dry-run`. The source is located relative to the actual script, regardless of working directory. Empty paths, `/`, and targets inside the source checkout are rejected.

## Version and configuration ownership

There is exactly one authoritative technical record of the installed version:

```text
.ai/foundation/VERSION
```

It is part of the staged Foundation, so replacement and rollback change or restore the version along with its files. The central repository's `VERSION` describes the available release. No separate `.ai/FOUNDATION_VERSION` is created or consulted.

New manifests contain configuration only:

```json
{
  "foundation": "digital-factory-ai-agents",
  "agent": "backend",
  "stack": "laravel",
  "security_agent": true,
  "audit_agent": true
}
```

The manifest is authoritative for configuration, not installed version or approval state. Only this Backend/Laravel combination with both roles enabled is supported. Missing, malformed, duplicate-key, foreign or unsupported manifests abort before writes. Required source files and ordinary `.ai/`, `foundation/` and `project/` directories must exist.

A small AWK validator deliberately supports **flat JSON objects with scalar values and plain ASCII identifier keys** (`[A-Za-z_][A-Za-z0-9_]*`). Whitespace and key order are flexible. Unknown string, number, boolean and null fields are retained. Strings support JSON escapes, but the required configuration values must use the literal spellings shown above. Nested objects/arrays and escaped/non-identifier keys fail safely before writes; arbitrary JSON mutation is not attempted. Move richer metadata to a separate team-managed file after review if an existing manifest uses these unsupported extensions. No unknown field is silently dropped.

For older installations, a legacy manifest `foundation_version` is deprecated and ignored, even if it disagrees with the installed VERSION. A successful replacement removes that field while retaining all other supported fields; JSON formatting may change. A same-version no-op leaves the legacy manifest unchanged and reports the authoritative source. Use `--force` to perform a backed-up same-version replacement and remove the field. A configuration-only manifest is left byte-for-byte unchanged by updates.

New initialization no longer copies `project-template/FOUNDATION_VERSION` into the project layer. Existing `.ai/project/FOUNDATION_VERSION` files remain untouched as legacy project-owned content and are never consulted for installed-version detection. They do not represent an implemented approval mechanism. These scripts do not record or infer team approval/adoption state; that is a separate future concern.

Both installed and available versions must use numeric `major.minor.patch`. Exact equality gives a no-op; numeric component comparison blocks downgrades unless forced, without integer-size assumptions. Prerelease/build suffixes are unsupported. A missing or malformed installed VERSION fails safely; the updater does not fall back to the manifest or project layer. The repository VERSION is not automatically bumped.

## Preview, integrity and force

Dry-run validates the same prerequisites and integrity as an update, reports versions, roles, proposed backup/replacement/legacy-migration actions and project preservation, and creates no files, directories or staging data. It never changes version metadata. Same-version installs report a successful no-op unless forced. Local modifications still block an unforced preview or no-op.

Do not edit `.ai/foundation/` directly. Use `.ai/project/` for project-specific constraints. Submit reusable improvements to the global Foundation repository.

New initialization and updates generate `.ai/foundation/checksums.sha256`, excluding the checksum file itself. Updates compare the current file inventory and hashes with the recorded inventory, detecting changed, missing and added files. Invalid checksum records also block an ordinary update. Checksum paths are never passed to a tool that opens them; only discovered Foundation files are hashed. This detects accidental changes, not malicious changes to both content and checksums.

An older installation without checksums warns that integrity was **not verified**, but may upgrade with a backup. Initialization warns and omits checksums if neither SHA utility is available. Updates require one of those utilities and otherwise fail before writes; they never silently skip integrity verification or generation.

With local modifications, move project customizations into `.ai/project/`, contribute reusable changes centrally, then retry. `--force` allows replacement after warning and retains the complete edited Foundation in a backup. It also permits same-version reinstall and downgrade; it never bypasses manifest, source or symlink validation.

## Staging, backups and rollback

The updater builds the complete compact Foundation in a unique `.ai/.foundation-stage-*` directory, using the shared explicit inventory, Markdown link adjustments and generated index. It validates checksums and VERSION and prepares any legacy manifest migration before moving the installed Foundation. Obsolete Foundation files disappear from the active installation rather than mixing releases.

Before replacement, the previous Foundation is copied to:

```text
.ai/backups/foundation-0.1.0-YYYYMMDD-HHMMSS/
```

The backup contains exactly the previous Foundation, without project context or manifest. Numeric suffixes distinguish collisions; an existing backup is never overwritten or automatically deleted. The old Foundation is moved into staging, the new Foundation is renamed into place, then any prepared legacy manifest is renamed over the old one. Normal updates do not write the configuration manifest. Successful updates print the backup path.

A failure after a complete backup attempts restoration and reports `Update failed.` and `Previous Foundation restored.` The backup remains available. Rollback restores `foundation/VERSION` together with the old files. Failed rollback reports `Automatic rollback could not be completed.` and `Manual recovery required from:` with recovery locations; staging recovery data is retained. Stop other writers and inspect those locations before restoring the Foundation. Never delete `.ai/project/` to recover. A failed backup copy leaves the active Foundation intact and may leave an incomplete backup directory; it is not reported as a successful update.

Directory renames prevent mixed versions but are not one filesystem transaction: there is a short interval without the active Foundation path. Shell failures and catchable termination signals trigger recovery. Power loss, SIGKILL and hostile concurrent filesystem changes cannot be recovered automatically. Use a quiescent local workspace without other installers, editors or agents accessing `.ai/`. No lock or crash-recovery journal is implemented. Keep enough free space for staging, backup and possible restoration.

The shared inventory includes Backend README and lifecycle prompts, Core, Laravel, shared, Security and Audit files. Arbitrary new central files are not copied; maintainers deliberately extend the inventory when adding dependencies. The initializer's older `--force` remains a nontransactional refresh that adds missing project templates and regenerates metadata; prefer the updater for existing installations.

## Team lifecycle

```text
Create project → Initialize Agent Foundation → Configure .ai/project/
→ Use Agent → Foundation evolves → Review CHANGELOG → Preview update
→ Update Foundation → Review and run agent evaluations → Continue development
```

For example: central release 0.2.0 → team reviews CHANGELOG → team runs `--dry-run` → team updates → project context remains preserved → team runs agent evaluations and resolves policy conflicts → team continues development. The command prints a changelog path when present but does not parse it, run evaluations or implement an approval workflow.

## Security and troubleshooting

Only Foundation files and configuration metadata are read. The project layer is inspected for file types, never opened for content. No `.env` content, application secrets or project executables are read or executed. No Git, PHP, Laravel, Composer, database, deployment, AI API or network commands run. No project code is sourced.

Symlinks and special nodes anywhere inside `.ai/`, including backups and project context, are rejected without following them. An `.env` entry inside `.ai/` is rejected by name before content reads. Source inventory paths also reject symlink components. Rename-based replacement avoids writing through existing hard links. These preflight checks do not protect against concurrent hostile path changes. Do not use an actively changing untrusted workspace or production mount.

- **Missing SHA utility:** make the platform's `sha256sum` or `shasum` available before updating.
- **Missing/invalid manifest:** restore configuration from project history; do not guess. Unsupported richer JSON requires explicit team review, not `--force`.
- **Missing/invalid VERSION:** restore the original installed VERSION with its corresponding Foundation files; never infer it from legacy metadata.
- **Missing source:** restore the trusted checkout; preflight leaves the installed Foundation intact.
- **Local changes:** review reported paths and deliberately resolve customizations or force with a backup.
- **Symlinks/special files:** use ordinary files/directories after team review; force does not bypass checks.
- **Permissions/disk failure:** read rollback diagnostics and preserve recovery material until restoration is verified.

Run `bash tests/scripts/test-init-project-agent.sh` and `bash tests/scripts/test-update-project-foundation.sh`. Tests use temporary projects and a copied central fixture. The update suite's Python harness invokes only shell operational scripts, including under a Unix-only PATH where Python, Node, PHP, Composer and jq are absent. Tests cover unchanged project bytes, version authority, legacy migration, dry-run, checksums, rollback, signal interruption and failed recovery. FIFO `.env` fixtures and forbidden-command stubs detect accidental secret reads and application/network commands. No agent runtime or Laravel sandbox validation is performed.
