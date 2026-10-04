# Contributing

Keep Boss Astra focused on instruction-based orchestration. The installable source
is [skills/boss-astra/SKILL.md](skills/boss-astra/SKILL.md); changes to a
personal installed copy do not update this repository.

## Make a change

1. Create a branch from `main`.
2. Keep changes scoped and preserve the existing skill name and invocation policy
   unless the change explicitly includes a migration.
3. Update installation instructions when package layout or compatibility changes.
4. Run the checks below and open a pull request describing the behavior and evidence.

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
git diff --check
```

For instruction changes, use the [behavioral scenarios](docs/evaluation.md).
Report what you actually observed, the host and requested model settings, and
checks that were unavailable. A simulated decision review is not an end-to-end
benchmark.

## Review expectations

- Preserve primary ownership, disjoint worker assignments, bounded retries, and
  existing authorization boundaries.
- Keep requirements portable. Do not include personal paths, private task logs,
  credentials, or user-specific forms of address.
- Add tests for meaningful validator behavior, not exact prose or heading matches.
- Keep third-party attribution when adapting upstream material. Keep the skill's
  bundled `LICENSE` and `THIRD_PARTY_NOTICES.md` identical to the root copies so
  standalone installs retain them.
- Avoid adding runtime dependencies, hooks, or external services without a clear
  need and an explicit change in scope.

Open [an issue](https://github.com/emjcsantos/boss_astra/issues) for bugs or focused
improvement proposals. Include a minimal, sanitized example of the behavior.

Contributions are provided under the repository's [MIT License](LICENSE).
