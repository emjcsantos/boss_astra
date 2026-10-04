# Boss Astra

A focused orchestration skill for Codex. The primary agent owns architecture,
integration, validation, and the final result, while independent work goes to
bounded subagents.

Boss Astra packages the `boss-astra` skill with explicit ownership, a bounded
retry policy, and context-aware recovery. It is an instruction-only community
project, not an OpenAI product. It includes no MCP servers, hooks, telemetry, or
API-key requirements.

## Install

Use a Codex client with plugin support:

```sh
codex plugin marketplace add emjcsantos/boss_astra --ref main
codex plugin add boss-astra@boss-astra
```

Start a new chat, select the **Boss Astra** skill from the skill picker, and
give it a concrete task. If the plugin does not appear, restart the client.
See the official [plugin packaging documentation](https://developers.openai.com/plugins/build/plugins)
for client-specific installation and marketplace support.

### Install only the skill

If your client does not support plugins, ask Codex's built-in installer:

```text
Use $skill-installer to install the skill at skills/boss-astra from
https://github.com/emjcsantos/boss_astra.
```

For manual installation, clone this repository and copy the
[`skills/boss-astra`](skills/boss-astra/SKILL.md) folder into your client's
user skill directory. Current Codex documentation uses `~/.agents/skills`;
some clients and the built-in installer use `$CODEX_HOME/skills`, normally
`~/.codex/skills`. Use the location supported by your client and avoid installing
duplicate copies with the same skill name. See [Codex skills](https://learn.chatgpt.com/docs/build-skills).

Copy the entire skill folder, including its license notices. Preserve any existing
local customizations before replacing an installed copy.

## Use

After selecting the skill, try:

```text
Plan and implement CSV export for the reporting page. Keep the existing API
compatible. Delegate only work that can proceed independently, validate the
integrated result, and report any checks that could not run.
```

With a standalone skill installation, you can invoke it explicitly:

```text
Use $boss-astra to investigate these three independent test failures and fix
their causes. Keep each worker's file ownership separate.
```

The skill also permits automatic selection when the host supports it. Explicit
user instructions, repository rules, and runtime permissions always take priority.
Planning-only requests stay within their requested scope.

## Routing defaults

| Responsibility | Preferred model | Effort |
|---|---|---|
| Primary coordination, integration, and acceptance | GPT-6 Astra | Current session setting |
| Bounded implementation, documentation, tests, or research | GPT-6 Luna | MAX |
| Standard multi-file implementation or debugging | GPT-6.1 Sol | HIGH |
| Complex architecture, migrations, or security work | GPT-6.1 Sol | XHIGH |
| Exceptionally difficult work | GPT-6.1 Sol | MAX |
| Independent review | GPT-6.1 Sol | Proportional to risk |

These are configurable workflow defaults, not model availability or performance
guarantees. The host must expose native subagents and the requested controls for
delegation. The skill cannot switch the primary model, enable unavailable tools,
or grant permissions. Without a usable delegation capability, the primary
continues work it can complete and reports any remaining limitation.

Small work stays local. Before dispatch, the primary settles dependencies and
assigns disjoint ownership. A reasoning failure gets one focused retry per lane:
Luna escalates to Sol, then the primary takes over. Missing context is supplied;
missing access is reported. Neither resets the retry budget or authorizes a
permission bypass. For long tasks, a compact task-local checkpoint supports
resumption without repeating completed work.

Read the [full skill](skills/boss-astra/SKILL.md) for fallback, review, and
acceptance rules. There are no claimed speed, cost, or quality benchmarks.

## Develop and validate

Python 3.10+ is needed for repository checks only; using the skill does not require
Python.

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
git diff --check
```

CI runs these checks on Linux and Windows. They validate package structure,
metadata, local document links, and validator behavior. They do not prove model
quality or end-to-end host compatibility. Behavioral changes should also be
checked against the [scenario checklist](docs/evaluation.md).

```text
plugin.json                          Portable plugin manifest
.agents/plugins/marketplace.json      Repository marketplace
skills/boss-astra/                    Installable skill and UI metadata
scripts/validate.py                   Offline package checks
tests/                               Validator regression tests
docs/evaluation.md                   Manual behavioral scenarios
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for scope and review expectations.

## Credits and license

Released under the [MIT License](LICENSE). This project builds on ideas from
[DannyMac180/astra-advisor](https://github.com/DannyMac180/astra-advisor),
[obra/superpowers](https://github.com/obra/superpowers), and Anthropic's
[context engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
Upstream copyright and license notices are retained in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
