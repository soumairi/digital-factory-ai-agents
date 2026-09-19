#!/usr/bin/env python3
"""Reproduce clean evidence using a pre-existing, hash-matching vendor directory."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
campaign=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2: raise SystemExit('Usage: python3 campaign/replay.py /path/to/existing/vendor')
vendor=Path(sys.argv[1]).resolve()
def verify(root,manifest):
    expected=json.loads(manifest.read_text())
    actual={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file()}
    if actual!=expected: raise SystemExit('Manifest mismatch: '+str(root))
verify(campaign/'candidate/final',campaign/'candidate/source-sha256.json')
verify(vendor,campaign/'candidate/vendor-sha256.json')
root=Path(tempfile.mkdtemp(prefix='backend-eval-001-replay-',dir='/private/tmp'))/'app'
shutil.copytree(campaign/'candidate/final',root)
shutil.copytree(vendor,root/'vendor')
print('Disposable replay: '+str(root),flush=True)
for command in [[sys.executable,str(campaign/'campaign/run-evidence.py'),str(root)],[sys.executable,str(root/'preflight/run.py'),'concurrency']]:
    completed=subprocess.run(command)
    if completed.returncode: raise SystemExit(completed.returncode)
