#!/usr/bin/env bash
set -euo pipefail
root=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
script="$root/scripts/init-project-agent.sh"
work=$(mktemp -d "${TMPDIR:-/tmp}/df-bootstrap-tests.XXXXXX")
trap 'rm -rf -- "$work"' EXIT
pass=0
ok() { pass=$((pass+1)); printf 'PASS %s\n' "$1"; }
reject() { if "$@" > "$work/error" 2>&1; then printf 'Expected failure: %s\n' "$*" >&2; exit 1; fi; }
mkdir "$work/project" "$work/dry" "$work/project with spaces"
"$script" --help > "$work/help"
grep -q -- '--force' "$work/help"; ok help
# Non-root working directory and '.' target.
(cd "$work/project" && "$script" backend laravel . > "$work/install")
[ -d "$work/project/.ai" ]; ok 'fresh initialization from another working directory'
ai="$work/project/.ai"
for f in shared/security-baseline.md backend/core/agent.md backend/laravel/security-rules.md security/agent.md audit/agent.md backend/prompts/analyze.md; do
    [ -f "$ai/foundation/$f" ]
done
[ ! -e "$ai/foundation/frontend" ]; ok 'selected content and dependencies only'
for f in "$root"/project-template/*; do [ -f "$ai/project/$(basename "$f")" ]; done
ok 'all project templates installed'
version=$(cat "$root/VERSION")
grep -q "\"foundation_version\": \"$version\"" "$ai/agent-manifest.json"
cmp "$root/VERSION" "$ai/foundation/VERSION"
ok 'manifest and copied VERSION match source'
reject "$script" backend laravel "$work/project"
ok 'repeat without force refused'
printf 'CUSTOM CONTEXT\n' > "$ai/project/project-context.md"
printf '0.0.1\n' > "$ai/project/FOUNDATION_VERSION"
printf 'stale\n' > "$ai/foundation/backend/core/agent.md"
rm "$ai/project/architecture.md"
"$script" backend laravel "$work/project" --force > "$work/force"
grep -q '^CUSTOM CONTEXT$' "$ai/project/project-context.md"
grep -q '^0.0.1$' "$ai/project/FOUNDATION_VERSION"
grep -q 'Backend Agent Contract' "$ai/foundation/backend/core/agent.md"
[ -f "$ai/project/architecture.md" ]; ok 'force refresh preserves project content/pin and adds missing template'
"$script" backend laravel "$work/dry" --dry-run > "$work/dry-output"
[ ! -e "$work/dry/.ai" ]; ok 'dry run writes nothing'
"$script" backend laravel "$work/project" --force --dry-run > "$work/force-dry"
grep -q PRESERVE "$work/force-dry"; ok 'force dry run lists preserved files'
reject "$script" frontend react "$work/dry"
grep -q 'Unsupported agent/stack combination' "$work/error"; ok 'unsupported configuration rejected'
reject "$script" backend laravel "$work/missing"
reject "$script" backend laravel ''
reject "$script" backend laravel /
ok 'invalid, empty and root targets rejected'
"$script" backend laravel "$work/project with spaces" > "$work/spaces"
[ -f "$work/project with spaces/.ai/agent-manifest.json" ]; ok 'spaces in target supported'
# A project .env is neither read for defaults nor changed/copied; external command traps.
printf 'BOOTSTRAP_SECRET_SENTINEL\n' > "$work/dry/.env"
cp "$work/dry/.env" "$work/env-before"
mkdir "$work/bin"
for cmd in git php composer curl wget node python python3 jq docker; do
    printf '#!/usr/bin/env bash\nprintf "unexpected command" >&2\nexit 99\n' > "$work/bin/$cmd"
    chmod +x "$work/bin/$cmd"
done
PATH="$work/bin:$PATH" "$script" backend laravel "$work/dry" > "$work/isolated"
cmp "$work/dry/.env" "$work/env-before"
! grep -R -q BOOTSTRAP_SECRET_SENTINEL "$work/dry/.ai" "$work/isolated"
ok 'no external/project commands; secret sentinel untouched and not copied'
mkdir "$work/link-target" "$work/outside"
ln -s "$work/outside" "$work/link-target/.ai"
reject "$script" backend laravel "$work/link-target" --force
ok 'linked .ai rejected'
ln -s "$work/outside" "$ai/foundation/escape"
reject "$script" backend laravel "$work/project" --force
rm "$ai/foundation/escape"
ok 'nested destination symlink rejected'
# Missing source preflight uses a copied foundation, never modifies the real one.
mkdir "$work/source"
cp -R "$root/scripts" "$root/shared" "$root/agents" "$root/project-template" "$work/source/"
cp "$root/VERSION" "$work/source/VERSION"
rm "$work/source/project-template/security-context.md"
mkdir "$work/preflight"
reject "$work/source/scripts/init-project-agent.sh" backend laravel "$work/preflight"
[ ! -e "$work/preflight/.ai" ]
grep -q 'security-context.md' "$work/error"
ok 'missing template fails before any target creation'
# Wrong destination type is also caught before global refresh.
printf 'KEEP\n' > "$ai/foundation/VERSION"
rm "$ai/project/commands.md"; mkdir "$ai/project/commands.md"
reject "$script" backend laravel "$work/project" --force
grep -q '^KEEP$' "$ai/foundation/VERSION"
ok 'type conflict preflight prevents partial refresh'
printf '\n%s tests passed. All test targets were temporary directories.\n' "$pass"
