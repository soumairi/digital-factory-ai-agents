# Analyze an Approved Backend Story

Apply the [Backend Agent contract](../core/agent.md), all linked core documents, and shared policies. This prompt grants no additional permissions.

Read the approved story and acceptance criteria, then inspect project context and existing architecture before proposing changes. Record the source and revision of governing context and distinguish observed conventions from assumptions. Trace affected behavior, data flows, access controls, and tests.

Assess every security topic and negative-test category in the [Definition of Done](../core/definition-of-done.md). Identify missing requirements, ownership/permission ambiguity, abuse cases, dependencies, and compatibility risks. Explicitly flag security ambiguity; never fill it with a permissive assumption.

Return a requirement summary, acceptance-criteria mapping, context references, affected architecture, risks, assumptions, and questions/blockers. Pause work dependent on unresolved ambiguity. Do not implement during analysis.
