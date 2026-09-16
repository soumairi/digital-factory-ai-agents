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

source "$script_dir/lib/foundation.sh"
configure_backend_laravel
add_group project-template project README.md project-context.md tech-stack.md architecture.md coding-conventions.md commands.md security-context.md compliance-context.md definition-of-done.md agent-overrides.md
for src in "${sources[@]}"; do check_source "$src"; done
version=$(cat "$source_root/VERSION")
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail 'VERSION must contain a numeric major.minor.patch version.'
# Reject all links/special nodes in the owned destination before any write.
[ ! -L "$ai" ] || fail "Symbolic destination is not allowed: $ai"
if [ -e "$ai" ]; then
    [ -d "$ai" ] || fail "Existing .ai is not a directory: $ai"
    $force || fail "Already exists: $ai. No changes made. Use --force to refresh global files and preserve project context."
    unsafe=$(find "$ai" \( -name .env -o \( ! -type d ! -type f \) \) -print)
    [ -z "$unsafe" ] || fail "Unsupported .env, symbolic link or special file under .ai: $unsafe"
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
for dst in "${destinations[@]}" README.md foundation/README.md foundation/checksums.sha256 agent-manifest.json; do check_destination "$dst"; done
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
    render_source "$src" | write_file "$dst"
done
cat <<EOF | write_file agent-manifest.json
{
  "foundation": "digital-factory-ai-agents",
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
EOF
foundation_index | write_file foundation/README.md
if command -v sha256sum >/dev/null 2>&1 || command -v shasum >/dev/null 2>&1; then
    foundation_checksums "$ai/foundation" | write_file foundation/checksums.sha256
else
    printf 'Warning: no SHA-256 tool available; integrity checksums not generated.\n' >&2
fi
printf 'Status: Initialization completed successfully.\nResult: %s/foundation/ and %s/project/\nNext steps:\n1. Complete .ai/project/project-context.md (Backend/Laravel and source revision).\n2. Complete .ai/project/architecture.md.\n3. Complete .ai/project/security-context.md.\n4. Review commands, Definition of Done, version adoption and evaluations.\n5. Run the Backend Agent using your selected approved AI runtime.\n' "$ai" "$ai"
