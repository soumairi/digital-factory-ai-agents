#!/usr/bin/env bash
# Filesystem-only bootstrap. Compatible with Bash 3.2+ on macOS/Linux.
set -euo pipefail
fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }
usage() {
    cat <<'EOF'
Usage: init-project-agent.sh backend laravel TARGET [--force] [--dry-run]
       init-project-agent.sh --help

TARGET must be an existing local project directory; '.' and spaces are supported.
Only backend/laravel is supported. No project commands or network requests run.
--force    Refresh managed foundation/README/manifest files; preserve every existing
           project file and add missing templates. No stale files are deleted.
--dry-run  Validate and print the complete plan without writing any files.
Options may appear before or after the three positional arguments.
EOF
}
force=false; dry=false; args=()
for arg in "$@"; do
    case "$arg" in
        --help|-h) usage; exit 0 ;;
        --force) force=true ;;
        --dry-run) dry=true ;;
        --*) fail "Unknown option: $arg" ;;
        *) args+=("$arg") ;;
    esac
done
[ "${#args[@]}" -eq 3 ] || { usage >&2; exit 1; }
agent=${args[0]}; stack=${args[1]}; target_arg=${args[2]}
case "$agent/$stack" in
    backend/laravel) ;;
    *) fail "Unsupported agent/stack combination: $agent/$stack
Currently supported: backend/laravel" ;;
esac
[ -n "$target_arg" ] || fail 'Target path is empty.'
[ -d "$target_arg" ] || fail "Target directory does not exist: $target_arg"
# Prefix relative paths to avoid treating names beginning with '-' as cd options.
case "$target_arg" in /*) ;; *) target_arg="./$target_arg" ;; esac
target=$(CDPATH= cd -P -- "$target_arg" && pwd -P)
[ "$target" != / ] || fail 'Refusing target /.'
[ ! -L "${BASH_SOURCE[0]}" ] || fail 'Invoke the actual script, not a symbolic link.'
script_dir=$(CDPATH= cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source_root=$(CDPATH= cd -P -- "$script_dir/.." && pwd -P)
case "$target/" in "$source_root/"*) fail 'Target must be outside the foundation source repository.' ;; esac
ai="$target/.ai"

# Explicit dispatch/content inventory: no recursive copy of arbitrary files or secrets.
sources=(); destinations=()
add() { sources+=("$1"); destinations+=("$2"); }
add_group() {
    local src=$1 dst=$2 name
    shift 2
    for name in "$@"; do add "$src/$name" "$dst/$name"; done
}
configure_backend_laravel() {
    add VERSION foundation/VERSION
    add_group shared foundation/shared engineering-principles.md security-baseline.md security-development-policy.md git-policy.md human-approval-policy.md audit-policy.md output-standards.md
    add agents/backend/README.md foundation/backend/README.md
    add_group agents/backend/core foundation/backend/core agent.md responsibilities.md workflow.md guardrails.md definition-of-done.md output-contract.md
    add_group agents/backend/prompts foundation/backend/prompts analyze.md plan.md implement.md test.md self-review.md
    add_group agents/backend/stacks/laravel foundation/backend/laravel README.md architecture.md coding-rules.md security-rules.md testing-rules.md database-rules.md api-rules.md commands.md
    add_group agents/security foundation/security README.md agent.md workflow.md guardrails.md vulnerability-checklist.md output-contract.md
    add_group agents/audit foundation/audit README.md agent.md workflow.md guardrails.md evidence-policy.md audit-checklist.md audit-report-template.md
    add_group project-template project README.md project-context.md tech-stack.md architecture.md coding-conventions.md commands.md security-context.md compliance-context.md definition-of-done.md agent-overrides.md FOUNDATION_VERSION
}
configure_backend_laravel
# Validate each component, so a linked source directory cannot redirect reads.
check_source() {
    local rel=$1 current=$source_root part
    local -a components
    IFS=/ read -r -a components <<< "$rel"
    for part in "${components[@]}"; do
        current="$current/$part"
        [ ! -L "$current" ] || fail "Symbolic source is not allowed: $rel"
    done
    [ -f "$current" ] && [ -r "$current" ] || fail "Missing or unreadable source file: $rel"
}
for src in "${sources[@]}"; do check_source "$src"; done
version=$(cat "$source_root/VERSION")
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail 'VERSION must contain a numeric major.minor.patch version.'
# Reject all links/special nodes in the owned destination before any write.
[ ! -L "$ai" ] || fail "Symbolic destination is not allowed: $ai"
if [ -e "$ai" ]; then
    [ -d "$ai" ] || fail "Existing .ai is not a directory: $ai"
    $force || fail "Already exists: $ai. No changes made. Use --force to refresh global files and preserve project context."
    unsafe=$(find "$ai" ! -type d ! -type f -print)
    [ -z "$unsafe" ] || fail "Unsupported symbolic link or special file under .ai: $unsafe"
fi
# Validate all future parent directories and leaf types, including generated files.
check_destination() {
    local rel=$1 leaf="$ai/$1" parent
    [ ! -e "$leaf" ] || [ -f "$leaf" ] || fail "Expected file at: $leaf"
    parent=$(dirname -- "$leaf")
    while [ "$parent" != "$target" ]; do
        [ ! -e "$parent" ] || [ -d "$parent" ] || fail "Expected directory at: $parent"
        parent=$(dirname -- "$parent")
    done
}
for dst in "${destinations[@]}" README.md foundation/README.md agent-manifest.json; do check_destination "$dst"; done
printf 'Digital Factory AI Agent Bootstrap\nTarget: %s\nAgent: %s\nStack: %s\nFoundation: v%s\n' "$target" "$agent" "$stack" "$version"
for dir in foundation/shared foundation/backend/core foundation/backend/prompts foundation/backend/laravel foundation/security foundation/audit project; do
    [ -d "$ai/$dir" ] || printf 'CREATE DIRECTORY %s\n' "$ai/$dir"
done
for ((i=0; i<${#sources[@]}; i++)); do
    dst=${destinations[i]}
    if [[ "$dst" == project/* ]] && [ -f "$ai/$dst" ]; then
        printf 'PRESERVE %s\n' "$ai/$dst"
    else
        printf 'COPY %s -> %s\n' "${sources[i]}" "$ai/$dst"
    fi
done
printf 'GENERATE %s/{README.md,agent-manifest.json,foundation/README.md}\n' "$ai"
if $dry; then printf 'Status: Dry-run complete; no files written.\n'; exit 0; fi
# Each file is replaced by rename, avoiding mutation through existing hard links.
# No recursive deletion or rollback that could destroy project edits.
temp_file=''
trap 'printf "Error: File creation failed near line %s. Partial installation may remain at %s; inspect before retrying with --force. Temporary file: %s\n" "$LINENO" "$ai" "$temp_file" >&2' ERR
write_file() {
    local dst=$1
    mkdir -p -- "$(dirname -- "$ai/$dst")"
    temp_file=$(mktemp "$ai/.bootstrap-file.XXXXXX")
    cat > "$temp_file"
    chmod 644 "$temp_file"
    mv -f -- "$temp_file" "$ai/$dst"
    temp_file=''
}
mkdir -p -- "$ai"
for ((i=0; i<${#sources[@]}; i++)); do
    src=${sources[i]}; dst=${destinations[i]}
    if [[ "$dst" == project/* ]] && [ -f "$ai/$dst" ]; then continue; fi
    # Adjust only relative link destinations for the compact install layout.
    case "$src" in
        agents/backend/stacks/laravel/*)
            sed -e 's|](../../core/|](../core/|g' -e 's|](../../README.md)|](../README.md)|g' -e 's|](../../../../shared/|](../../shared/|g' "$source_root/$src" | write_file "$dst" ;;
        agents/backend/core/*|agents/backend/prompts/*)
            sed -e 's|](../../../shared/|](../../shared/|g' -e 's|](../../../README.md#|](../../README.md#|g' "$source_root/$src" | write_file "$dst" ;;
        agents/backend/README.md|agents/security/*|agents/audit/*)
            sed -e 's|](../../shared/|](../shared/|g' -e 's|](../../README.md#|](../README.md#|g' -e 's|](stacks/laravel/|](laravel/|g' "$source_root/$src" | write_file "$dst" ;;
        project-template/FOUNDATION_VERSION) printf '%s\n' "$version" | write_file "$dst" ;;
        *) cat "$source_root/$src" | write_file "$dst" ;;
    esac
done
cat <<EOF | write_file agent-manifest.json
{
  "foundation": "digital-factory-ai-agents",
  "foundation_version": "$version",
  "agent": "backend",
  "stack": "laravel",
  "security_agent": true,
  "audit_agent": true
}
EOF
cat <<'EOF' | write_file README.md
# Project AI Agent Foundation

This project uses the Digital Factory AI Agent Foundation.

Backend Agent Core + Laravel Stack Profile + Global Engineering & Security Policies
+ Project Context = Project Laravel Backend Agent.

- [foundation/README.md](foundation/README.md) indexes versioned global rules.
- [project/project-context.md](project/project-context.md) starts project-specific context and constraints.
- agent-manifest.json records the installed version and selected Backend/Laravel configuration.

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

A force refresh preserves every existing project file, including FOUNDATION_VERSION.
Compare that project adoption pin with foundation/VERSION and the manifest after
refresh; a mismatch requires explicit review/adoption before using the new rules.
Record the approved source revision in project context. Run required evaluations
using the central repository's evals/backend specifications and isolated fixtures;
those evaluation specifications are not copied by this minimal installer.
EOF
{
    printf '# Installed Foundation\n\nRead [Backend](backend/README.md), [Laravel](backend/laravel/README.md), [Security](security/README.md) and [Audit](audit/README.md).\n\n## Shared policy map\n\n'
    for policy in engineering-principles security-baseline security-development-policy git-policy human-approval-policy audit-policy output-standards; do
        printf -- '- [%s](shared/%s.md)\n' "$policy" "$policy"
    done
} | write_file foundation/README.md
printf 'Status: Initialization completed successfully.\nResult: %s/foundation/ and %s/project/\nNext steps:\n1. Complete .ai/project/project-context.md (Backend/Laravel and source revision).\n2. Complete .ai/project/architecture.md.\n3. Complete .ai/project/security-context.md.\n4. Review commands, Definition of Done, version adoption and evaluations.\n5. Run the Backend Agent using your selected approved AI runtime.\n' "$ai" "$ai"
