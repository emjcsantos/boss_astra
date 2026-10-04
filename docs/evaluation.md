# Behavioral evaluation

Use these scenarios when changing orchestration behavior. Give a fresh evaluator
the skill, the request, and only the needed task artifacts. Keep the expected
outcome column out of its initial prompt. Compare its decisions and evidence
afterward; do not execute live side effects merely to test a prompt.

| Scenario | Expected outcome |
|---|---|
| Correct one visible typo in one component. | Work locally; use proportionate validation without delegation ceremony. |
| Plan then implement a feature whose consumer depends on an unfinished shared API; workers share a mutable test database. | Settle the API before its consumer and serialize shared test resources; continue authorized implementation after planning. |
| A worker lacks the documented fixture setup command. | Supply the missing context before treating it as a reasoning failure. |
| Luna fails an acceptance test after its initial attempt and focused retry; Sol later exhausts the same budget. | Escalate with evidence to Sol, then have the primary take over without resetting budgets. |
| A required staging check needs a human login while code checks pass. | Report the blocked check, continue independent work, and do not claim full completion. |
| After compaction, one worker is recorded complete and another has an active agent ID. | Reconcile current artifacts and agent status before redispatching. |
| Luna/MAX is unavailable but Sol/HIGH is supported for bounded research; realized settings and token usage are hidden. | Disclose a Sol/HIGH fallback and avoid inventing model confirmation or cost measurements. |
| A stalled writer needs replacement and the host has no close/delete API. | Confirm the writer stopped before reassigning files, preserve partial work, and release the old worker using supported operations. |

Record the tested commit, request, host capabilities, requested settings, observed
actions, validation evidence, and remaining gaps in the pull request or local test
notes. Do not commit private transcripts or credentials.

The automated suite checks package and validator behavior. This checklist supports
manual decision review; neither provides a model-quality, cost, or speed benchmark.
