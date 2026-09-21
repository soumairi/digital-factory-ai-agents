# Output Standards

Agent outputs must be clear, concise, reviewable, and grounded in observed evidence.

For a change or review, report:

1. The intended outcome and scope.
2. Files or artifacts created, changed, or reviewed, with usable references.
3. Key decisions and relevant rationale.
4. Validation performed and results, distinguishing passed, failed, and unperformed checks.
5. Assumptions, unresolved findings, limitations, and required approvals.
6. Completion status and any blocked work.

- Scale detail to the task; do not generate unnecessary documentation.
- Distinguish facts, recommendations, assumptions, and open decisions.
- Never claim an action, check, approval, or review occurred without evidence.
- Do not expose secrets or confidential project data in summaries, logs, or reusable examples.
- Mark incomplete policy decisions with `TBD` and state the operational consequence if unresolved.
- Identify the foundation version and applicable profile/context revisions when future composed agents report work, so their governing rules are traceable.
- Stop at the authorized phase boundary; do not silently start follow-on work.

## Further definition

- **TBD:** Minimal reusable review and evidence templates, if recurring use demonstrates a need.
- **TBD:** Machine-readable output formats only when a concrete integration requires them.
