# Security Development Policy

Implementation roles own secure development. Independent Security and Audit review provides a second line of control; it does not replace that responsibility.

- Identify relevant assets, trust boundaries, entry points, and misuse risks before making security-sensitive changes.
- Apply input validation, appropriate authorization, safe error handling, and data minimization wherever relevant.
- Never hard-code credentials or log secrets. Use established, reviewed cryptographic mechanisms rather than custom cryptography.
- Introduce dependencies only when justified; review their source, maintenance, license compatibility, and known vulnerabilities using the consuming project's approved process.
- Verify changed behavior and relevant failure paths. Select security checks appropriate to the impact, such as secret detection, dependency analysis, static analysis, or targeted tests.
- Report which checks ran, their results, and any coverage gaps. Do not claim security assurance from checks that were not performed.
- Route changes to authentication, authorization, secrets, sensitive data handling, infrastructure permissions, or security controls to independent Security review before human integration approval.
- Block progression of affected work when material security findings remain unresolved. Agents cannot accept security risk on behalf of humans.
- Record remediation and obtain independent verification of security finding closure.

## Further definition

- **TBD:** Shared finding severity definitions and risk acceptance authority.
- **TBD:** Minimum check requirements by change risk and evidence required for risk acceptance.
- **Project layer responsibility:** Select concrete tools and commands without weakening this baseline.

Until risk acceptance authority and criteria are defined, unresolved material findings remain blocking. Absolute prohibitions in shared policies cannot be waived by risk acceptance.
