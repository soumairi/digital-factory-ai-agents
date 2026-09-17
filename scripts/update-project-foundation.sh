#!/usr/bin/env bash
# Filesystem-only updater, Bash 3.2+ and standard macOS/Linux utilities.
set -euo pipefail
export LC_ALL=C
fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }
usage() {
    cat <<'USAGE'
Usage: update-project-foundation.sh TARGET [--dry-run] [--force]
       update-project-foundation.sh --help
Options may precede or follow TARGET. Only backend/laravel is supported.
--dry-run  Validate and preview without writes.
--force    Allow reinstall, downgrade, or replacement of local Foundation edits.
Installed version authority: .ai/foundation/VERSION. No Python or jq required.
USAGE
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
[ "${#args[@]}" -eq 1 ] || { usage >&2; exit 1; }
[ -n "${args[0]}" ] || fail 'Target path is empty.'
target_arg=${args[0]}
[ -d "$target_arg" ] || fail 'Target directory does not exist.'
case "$target_arg" in /*) ;; *) target_arg="./$target_arg" ;; esac
target=$(CDPATH= cd -P -- "$target_arg" && pwd -P)
[ "$target" != / ] || fail 'Refusing target /.'
[ ! -L "${BASH_SOURCE[0]}" ] || fail 'Invoke the actual script, not a symbolic link.'
script_dir=$(CDPATH= cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source_root=$(CDPATH= cd -P -- "$script_dir/.." && pwd -P)
case "$target/" in "$source_root/"*) fail 'Target must be outside the foundation source repository.' ;; esac
source "$script_dir/lib/foundation.sh"
ai="$target/.ai"; foundation="$ai/foundation"; manifest="$ai/agent-manifest.json"
[ ! -L "$ai" ] && [ -d "$ai" ] || fail 'Expected ordinary .ai directory.'
unsafe=$(find "$ai" \( -name .env -o \( ! -type d ! -type f \) \) -print)
[ -z "$unsafe" ] || fail "Refusing .env, symbolic link or special file under .ai: $unsafe"
for dir in "$foundation" "$ai/project"; do [ -d "$dir" ] || fail "Missing directory: $dir"; done
[ ! -e "$ai/backups" ] || [ -d "$ai/backups" ] || fail 'Expected backups directory.'
[ -f "$manifest" ] || fail 'Missing agent-manifest.json.'
# A bounded grammar, not regex extraction from arbitrary JSON. No target code runs.
legacy=$(awk -v mode=legacy -f "$script_dir/lib/manifest.awk" "$manifest") || fail 'Invalid or unsupported manifest. Expected backend/laravel with both roles enabled and flat scalar JSON fields with plain ASCII keys.'
configure_backend_laravel
for src in "${sources[@]}"; do check_source "$src"; done
[ -f "$foundation/VERSION" ] || fail 'Missing installed foundation/VERSION.'
installed=$(cat "$foundation/VERSION")
version=$(cat "$source_root/VERSION")
for v in "$installed" "$version"; do
    [[ "$v" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail 'VERSION must contain numeric major.minor.patch.'
done
command -v sha256sum >/dev/null 2>&1 || command -v shasum >/dev/null 2>&1 || fail 'A SHA-256 utility (sha256sum or shasum) is required for updates.'
printf 'Digital Factory AI Foundation Update\nTarget project: %s\nInstalled Foundation: %s\nAvailable Foundation: %s\nAgent: backend\nStack: laravel\nSecurity Agent: enabled\nAudit Agent: enabled\n' "$target" "$installed" "$version"
[ ! -f "$source_root/CHANGELOG.md" ] || printf 'Review Foundation changes before adoption: %s/CHANGELOG.md\n' "$source_root"
[ -z "$legacy" ] || printf 'Legacy manifest foundation_version is ignored; foundation/VERSION is authoritative. The legacy field will be removed on replacement.\n'
if [ -e "$foundation/checksums.sha256" ]; then
    [ -f "$foundation/checksums.sha256" ] || fail 'Expected checksums.sha256 file.'
    actual=$(foundation_checksums "$foundation") || fail 'Could not calculate installed checksums.'
    expected=$(LC_ALL=C sort "$foundation/checksums.sha256")
    if [ "$actual" != "$expected" ]; then
        printf 'Local modifications were detected inside .ai/foundation/.\n'
        # Compare inventories, never pass untrusted checksum paths to checksum -c.
        diff <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") || :
        printf 'Project-specific customization must live under .ai/project/.\n1. Move project-specific changes into .ai/project/.\n2. Contribute reusable changes back to digital-factory-ai-agents.\n3. Retry the update.\n'
        $force || fail 'Update blocked; use --force only after reviewing changes.'
        printf 'WARNING: local Foundation modifications will not be preserved in the active Foundation; a complete backup will be kept.\n'
    else
        printf 'Installed Foundation integrity verified.\n'
    fi
else
    printf 'WARNING: no checksums.sha256; local integrity was NOT verified. A backup will be created for the update.\n'
fi
# Compare arbitrary-length numeric components without shell integer overflow.
if awk -v old="$installed" -v new="$version" 'BEGIN {
    split(old,a,"."); split(new,b,".")
    for(i=1;i<=3;i++) {
        sub(/^0+/,"",a[i]); sub(/^0+/,"",b[i])
        if(length(a[i])!=length(b[i])) exit !(length(a[i])>length(b[i]))
        if("x" a[i] != "x" b[i]) exit !("x" a[i] > "x" b[i])
    }
    exit 1
}'; then
    $force || fail 'Downgrade refused; use --force to allow it.'
fi
if [ "$installed" = "$version" ] && ! $force; then
    printf 'Foundation is already up to date.\n'
    ! $dry || printf 'No files were modified because --dry-run was used.\n'
    exit 0
fi
base="$ai/backups/foundation-$installed-$(date +%Y%m%d-%H%M%S)"
backup=$base; suffix=0
while [ -e "$backup" ]; do suffix=$((suffix+1)); backup="$base-$suffix"; done
printf 'Foundation backup: would create %s\nFoundation: would replace %s\nVersion authority: would replace foundation/VERSION with %s\n' "$backup" "$foundation" "$version"
if [ -n "$legacy" ]; then printf 'Manifest: would remove legacy foundation_version (configuration retained).\n'; else printf 'Manifest: preserved (configuration only).\n'; fi
printf 'Project context: PRESERVED / NOT MODIFIED (.ai/project/)\n'
if $dry; then printf 'No files were modified because --dry-run was used.\n'; exit 0; fi
stage=''; committed=false; backup_ready=false
cleanup() {
    status=$?
    trap - EXIT HUP INT TERM
    if [ "$status" -ne 0 ]; then
        printf 'Update failed.\n' >&2
        if $backup_ready && ! $committed; then
            # Retain backup; restore using a staged copy and rename.
            if { [ ! -e "$foundation" ] || mv -- "$foundation" "$stage/failed-foundation"; } &&
                cp -pR -- "$backup" "$stage/restore" && mv -- "$stage/restore" "$foundation"; then
                printf 'Previous Foundation restored.\n' >&2
            else
                printf 'Automatic rollback could not be completed.\nManual recovery required from:\n%s\nStaging recovery files: %s\n' "$backup" "$stage" >&2
                exit "$status"
            fi
        fi
    fi
    # Only this invocation's mktemp directory can be deleted.
    if [ -n "$stage" ]; then rm -rf -- "$stage"; fi
    exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP
stage=$(mktemp -d "$ai/.foundation-stage-XXXXXX")
mkdir -- "$stage/foundation"
for ((i=0;i<${#sources[@]};i++)); do
    dst="$stage/${destinations[i]}"
    mkdir -p -- "$(dirname -- "$dst")"
    render_source "${sources[i]}" > "$dst"
done
foundation_index > "$stage/foundation/README.md"
foundation_checksums "$stage/foundation" > "$stage/foundation/checksums.sha256"
actual=$(foundation_checksums "$stage/foundation")
[ "$actual" = "$(cat "$stage/foundation/checksums.sha256")" ] || fail 'Staged checksum verification failed.'
[ "$(cat "$stage/foundation/VERSION")" = "$version" ] || fail 'Staged VERSION mismatch.'
if [ -n "$legacy" ]; then
    cp -p -- "$manifest" "$stage/previous-agent-manifest.json"
    cp -p -- "$manifest" "$stage/agent-manifest.json"
    awk -f "$script_dir/lib/manifest.awk" "$manifest" > "$stage/agent-manifest.json"
fi
mkdir -p -- "$ai/backups"
# Build a complete backup before replacement; mkdir reserves the name exclusively.
mkdir -- "$backup"
cp -pR -- "$foundation/." "$backup/"
backup_ready=true
mv -- "$foundation" "$stage/previous-foundation"
mv -- "$stage/foundation" "$foundation"
if [ -n "$legacy" ]; then mv -f -- "$stage/agent-manifest.json" "$manifest"; fi
committed=true
printf 'Foundation update completed successfully.\nBackup: %s\nProject context: PRESERVED / NOT MODIFIED\n' "$backup"
