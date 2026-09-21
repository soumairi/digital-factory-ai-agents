#!/usr/bin/env python3
"""Declared evaluation asset freeze. Never imports or executes inventoried code."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = 'evals/backend/governed-inventory.json'
DIRECTORIES = ('evals/backend', 'agents/backend/core', 'agents/backend/stacks/laravel',
               'agents/security', 'agents/audit', 'shared', 'tests/adapters', 'tests/evals')
FILES = ('VERSION', 'README.md', 'CHANGELOG.md', 'docs/14-backend-evaluation-protocol.md',
         'docs/09-update-foundation.md', 'docs/evaluation-freeze.md')
# Source-like files are NEVER ignored, including under a runtime directory.
PROTECTED = {'.py', '.sh', '.json', '.md', '.php', '.yaml', '.yml', '.toml', '.ini', '.xml'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ephemeral(path):
    """Narrow, documented runtime exceptions; no blanket directory exemptions."""
    p = PurePosixPath(path)
    if p.suffix in PROTECTED:
        return False
    if p.name == '.DS_Store' or p.suffix == '.pyc':
        return True
    if p.name == '.coverage':
        return True
    if '.pytest_cache' in p.parts and p.name in {'CACHEDIR.TAG', '.gitignore', 'nodeids', 'lastfailed', 'stepwise'}:
        return True
    # Only plain temporary test output, never source/manifests/specifications.
    if 'tmp' in p.parts and p.suffix in {'.log', '.txt'}:
        return True
    return False


def asset_type(path):
    if '/faults/' in path: return 'fault-definition'
    if path.endswith('expected-results.json'): return 'expected-results'
    if 'manifest' in Path(path).name or path.endswith('checksums.json'): return 'manifest'
    if '/fixtures/' in path or path.endswith('/fixture.json'): return 'fixture'
    if path.startswith('evals/backend/BE-') and path.endswith('.md'): return 'evaluation-specification'
    if path.startswith('tests/'): return 'framework-test'
    if path.endswith(('.py', '.sh')) or '/tests/' in path or '/common/' in path: return 'verifier'
    if '/adapters/' in path: return 'adapter-source'
    return 'foundation-evaluation-policy'


def discover(root):
    """Discover prohibited additions, not a mutable definition of frozen assets."""
    found = set()
    for name in DIRECTORIES + FILES:
        base = root / name
        if base.is_symlink(): raise ValueError('Symlink prohibited: ' + name)
        if not base.exists(): raise ValueError('Missing governed scope: ' + name)
        paths = base.rglob('*') if base.is_dir() else [base]
        for p in paths:
            rel = p.relative_to(root).as_posix()
            if p.is_symlink(): raise ValueError('Symlink prohibited: ' + rel)
            if p.is_file() and rel != SNAPSHOT and not ephemeral(rel): found.add(rel)
    return found


def build(root):
    version = (root / 'VERSION').read_text().strip()
    return {'schema_version': 1, 'foundation_version': version,
            'assets': [{'path': p, 'asset_type': asset_type(p), 'sha256': digest(root / p),
                        'reference': 'Foundation ' + version} for p in sorted(discover(root))]}


def validate(root=ROOT, expected_sha256=None):
    root = Path(root)
    snapshot = root / SNAPSHOT
    if snapshot.is_symlink(): raise ValueError('Snapshot symlink prohibited')
    frozen_hash = digest(snapshot)
    if expected_sha256 is not None and frozen_hash != expected_sha256:
        raise ValueError('Pinned governed snapshot changed')
    data = json.loads(snapshot.read_text())
    if set(data) != {'schema_version', 'foundation_version', 'assets'} or data['schema_version'] != 1:
        raise ValueError('Unsupported governed inventory schema')
    if data['foundation_version'] != (root / 'VERSION').read_text().strip():
        raise ValueError('Foundation version changed')
    actual = discover(root)  # Reject symlinked paths before reading declared files.
    declared = set()
    for entry in data['assets']:
        if set(entry) != {'path', 'asset_type', 'sha256', 'reference'}:
            raise ValueError('Invalid governed entry')
        name = entry['path']; p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or p.as_posix() != name or name in declared:
            raise ValueError('Unsafe or duplicate inventory path')
        if name not in actual:
            raise ValueError('Entry outside governed inventory or missing: ' + name)
        declared.add(name)
        if entry['asset_type'] != asset_type(name) or entry['reference'] != 'Foundation ' + data['foundation_version']:
            raise ValueError('Invalid governed classification/reference: ' + name)
        target = root / name
        if target.is_symlink() or not target.is_file() or digest(target) != entry['sha256']:
            raise ValueError('Governed asset changed or missing: ' + name)
    # Unlisted non-runtime files under these roots are prohibited until reviewed/refrozen.
    if declared != actual:
        raise ValueError('Undeclared or omitted governed assets: ' + ', '.join(sorted(declared ^ actual)))
    return frozen_hash


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'build'])
    parser.add_argument('--expected-sha256')
    args = parser.parse_args()
    if args.action == 'build':
        if args.expected_sha256: parser.error('Pin applies only to check')
        (ROOT / SNAPSHOT).write_text(json.dumps(build(ROOT), indent=2) + '\n')
    try:
        print(json.dumps({'status': 'PASS', 'freeze': validate(expected_sha256=args.expected_sha256)}))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)})); return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
