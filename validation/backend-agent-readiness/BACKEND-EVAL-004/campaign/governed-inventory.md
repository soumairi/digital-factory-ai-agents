# Governed inventory
External campaign pin: `41948468644c73d9791729354b3abb2e63bc04fc8d25812d96ac22ea0296af92`. Copied inventory: governed-inventory.json (283 assets). Source authority: evals/backend/governed-inventory.json and evals/backend/freeze.py. Check with python3 -B evals/backend/freeze.py check --expected-sha256 41948468644c73d9791729354b3abb2e63bc04fc8d25812d96ac22ea0296af92 at boundaries. Never build/re-freeze during execution.

Only documented ephemeral exceptions are excluded. Candidate/runtime dependencies have separate hashes. Historical-sha256.json pins 500 historical campaign and review files. Generated campaign evidence is outside governed roots. Hash checks cannot establish cryptographic execution independence or exclude transient restored mutation.
