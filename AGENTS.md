# Repository guidance

This repository publishes the Boss Astra plugin and its `boss-astra` skill.

- Treat `skills/boss-astra/` as the canonical distributable source. Do not edit
  personal installed copies as part of repository maintenance.
- Keep the plugin instruction-only unless the user authorizes runtime additions.
- Preserve the skill identifier and automatic invocation policy unless a migration
  is explicitly requested. Let user and project instructions set personal style.
- Use a task branch. Keep Git and publication operations with the primary agent.
- Give parallel workers disjoint ownership and preserve concurrent edits.
- Keep public files free of private context, machine paths, credentials, and logs.
- Preserve upstream license notices and distinguish tested behavior from assumptions.

Validate changes with `python scripts/validate.py`,
`python -m unittest discover -s tests -v`, and `git diff --check`.
Install development dependencies from `requirements-dev.txt` when needed.
For skill behavior changes, also review the affected cases in `docs/evaluation.md`.
Do not claim behavioral or performance proof from metadata checks alone.
