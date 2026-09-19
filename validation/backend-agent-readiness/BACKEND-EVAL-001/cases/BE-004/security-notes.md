# BE-004 Security evidence

| Item | Status |
|---|---|
| Positive and denied behavior | Two tenants with two owners each, same/cross-tenant reads/writes, scoped list/count, nested parent-child mismatches and legitimate controls |
| State/output evidence | CampaignTest.php and final-junit.xml |
| Sensitive controls | Independently reproducible source/tests retained; independent verification NOT_RUN |
| Critical / High observed | 0 / 0 in same-author execution; not an independent all-clear |
| New independent findings | Unknown — no independent reviewer assigned |
| Shared security checklist | detailed/security-control-assessment.md |
| Fault isolation | Separate /private/tmp fault-* copies; clean source not overwritten |
| Independent clearance | NOT_VERIFIED; self-review is not substituted |

Original tenant/owner scenario exercised, not adapted from customer listing. Independent verification missing.
