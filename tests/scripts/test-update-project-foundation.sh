#!/usr/bin/env bash
set -euo pipefail
root=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
exec python3 -I "$root/tests/scripts/test_update_foundation.py" "$root"
