---
name: boss-astra
license: MIT
description: Orchestrate authorized multi-agent implementation, integration, research, or review with complexity-based Luna/Sol routing and primary-owned acceptance. Use when bounded independent work benefits from delegation; keep trivial and tightly coupled work local.
---

# Boss Astra

Follow current user instructions and applicable AGENTS.md. This skill governs delegation, not scope, permissions, global configuration, or publication authority.

## Primary ownership

Prefer GPT-6 Astra (`gpt-6-astra`) as primary. The primary owns architecture, task division, integration, final validation, Git operations, and reporting; it may implement directly.

A skill cannot switch the session model or effort. Continue with the current primary without a model-confirmation gate. Distinguish requested settings from runtime-observed settings; claim only what authoritative metadata exposes. Do not inspect private logs merely to discover unavailable telemetry.

## Choose the execution shape

Classify work using project definitions. Without them, use trivial for cosmetic edits, narrow for behavior within one module, standard for related multi-file behavior, and high risk for security, authentication, payments, migrations, deployment, or external mutations. Trivial stays local; narrow usually stays local. Delegate only authorized, bounded work whose independent progress justifies coordination and review overhead.

- Assign disjoint file ownership; resolve dependencies and shared interfaces before dispatching their consumers. Different files can still share state, fixtures, or build outputs; serialize those resources.
- Batch similar small edits. Avoid duplicating assigned exploration or implementation in the primary or another worker; an intentional independent review is distinct.
- Respect available slots and user budgets. Workers do not delegate further unless the primary explicitly assigns that authority within the user's authorization.
- Continue useful independent primary work while workers run. Use event notifications or bounded waits consistent with the host's responsiveness requirements; avoid repeated status polling.

For plan-then-implement requests, continue into implementation without inventing an approval gate. Planning-only requests remain read-only unless saving a plan was authorized.

## Worker routing

Use live tool-supported models and efforts. These are configurable routing defaults, not public performance rankings.

| Work | Model | Effort |
|---|---|---|
| Bounded implementation, documentation, tests, or research | `gpt-6-luna` | `max` |
| Standard multi-file implementation or debugging | `gpt-6.1-sol` | `high` |
| Complex architecture, integration-sensitive debugging, migrations, or security | `gpt-6.1-sol` | `xhigh` |
| Exceptionally difficult, ambiguous, or high-consequence work | `gpt-6.1-sol` | `max` |
| Independent diagnosis, validation, or review | `gpt-6.1-sol` | `medium`, `high`, `xhigh`, or `max` by risk |
| Remaining diagnosis, revisions, and validation after Sol fails | Astra primary | Current session setting |

Luna uses MAX. If its model or MAX effort is unavailable, promote to Sol; if Sol is unavailable, use Astra. Reassess effort for the new model: Sol HIGH for bounded/standard fallback work, XHIGH for complex work, MAX for exceptional work. For an unavailable effort on Sol/Astra, choose the nearest supported effort at or above it, or disclose the highest available effort's limitation. Report substitutions and reasons; honor explicit restrictions against them. If no capable lane exists, report the concrete blocker and continue independent primary work.

## Delegation contract

Give each worker only the context needed for its assignment:

- Objective, observable acceptance criteria, and relevant source/artifact paths.
- Owned files or responsibility, forbidden files, dependencies, and settled interfaces.
- Constraints, validation commands, and ownership of shared test resources.
- Retry limit: one initial attempt plus one focused retry per lane; no Git operations or unassigned delegation.

Tell editing workers: "You are not alone in the codebase. Preserve others' edits, do not revert unrelated work, and adapt to concurrent changes. Edit only your assigned files."

Use native subagents, not separate user-visible chats or nested CLI agents. With model/effort overrides, use `fork_turns: "none"` or a bounded turn count supported by the current API. Do not select a role that overrides the intended routing.

Require a concise return: `done`, `done_with_concerns`, `needs_context`, or `blocked`; changed files or findings; actual validation commands/results; concerns and remaining gaps. Link large artifacts instead of pasting histories. A successful dispatch or claimed completion is not acceptance.

## Supervise and recover

Supply missing context before treating `needs_context` as a reasoning failure. For `blocked`, distinguish access/environment limitations from excessive scope or insufficient reasoning: repair authorized prerequisites, split the task, or escalate as appropriate. A stronger model cannot supply missing permission or evidence.

For failed work, allow one focused retry with the actual failure, attempted fix, validation output, and remaining blocker. Retry only when the approach or evidence changes. Escalate Luna to Sol after the retry, or earlier if misclassified; after Sol's retry, the primary takes over. Fresh agents and review rounds do not reset the assignment's retry budget. Do not escalate through an unchanged environment or authorization blocker.

Track assignments in the existing task tracker. For work spanning compaction or resumption, keep a compact task-local checkpoint in authorized scratch space: goal, dependencies, owners/agent IDs, completed work and evidence, attempts, blockers, and next action. Reconcile it with current files and agent status before redispatching. Avoid new ledgers for short tasks and global memory writes without user request.

Before reassigning files, confirm the old writer has stopped; preserve partial edits. After handoff, close the worker if supported, otherwise release it and leave it idle. Do not invent a close API or treat interruption as deletion.

## Integration and acceptance

Inspect the actual scoped changes and evidence, then perform proportionate primary validation. Check both requirements coverage and correctness, including omissions and integration risks. Distinguish baseline failures, skipped checks, and new regressions. Repeat successful checks only when later edits or unresolved concerns justify it; serialize shared outputs.

Use fresh-context independent review when risk or the user warrants it. Forbid reviewer edits. Supply requirements, actual changes, interfaces, and validation evidence without prescribing conclusions. Require actionable findings with file references or a `ship` / `fix-first` / `rethink` recommendation. Review is advisory: the primary resolves material findings and verifies affected surfaces before acceptance. Agent agreement is not proof; fresh context is not model-family independence or OS-enforced read-only isolation.

Follow project Git/publication rules. Use the user's preferred style and report concisely: outcome, evidence, branch/files when substantial, and deferred or blocked work. Do not claim completion with required work outstanding. Cost/speed claims require measured evidence; do not impose cost receipts on ordinary tasks.
