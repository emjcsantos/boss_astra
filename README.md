# Boss Astra

A Codex plugin with one orchestration skill: Astra handles planning and final validation,
while Luna and Sol take on bounded tasks when delegation helps.

## Install

```sh
codex plugin marketplace add emjcsantos/boss_astra --ref main
codex plugin add boss-astra@boss-astra
```

## Use

Select **Boss Astra** in the Codex skill picker, then describe your task.
The skill uses the models available in your Codex environment.

## Models and effort

| Responsibility | Preferred model | Reasoning effort |
|---|---|---|
| Architecture, task division, integration, final validation, Git operations, and reporting | GPT-6 Astra | Current session setting |
| Bounded implementation, documentation, tests, or research | GPT-6 Luna | MAX |
| Standard multi-file implementation or debugging | GPT-6.1 Sol | HIGH |
| Complex architecture, integration-sensitive debugging, migrations, or security | GPT-6.1 Sol | XHIGH |
| Exceptionally difficult, ambiguous, or high-consequence work | GPT-6.1 Sol | MAX |
| Independent diagnosis, validation, or review | GPT-6.1 Sol | MEDIUM, HIGH, XHIGH, or MAX, based on risk |
| Remaining work after Sol exhausts its retry | Astra primary | Current session setting |

These are routing defaults. The skill cannot change the primary session's model
or effort, so it works with the current primary. Delegation uses the models and
effort controls exposed by your Codex environment.

## How delegation works

Small tasks stay with the primary. For larger tasks, the primary delegates only
independent work with clear file ownership, acceptance criteria, and validation
requirements. It reviews the returned work and validates the integrated result.

Each worker gets one initial attempt and one focused retry. If Luna cannot solve
or validate the assignment, it escalates to Sol with the failure evidence. After
Sol's focused retry, the primary takes over. Missing context is supplied first;
access or permission blockers are handled separately from reasoning failures.

If Luna or its MAX setting is unavailable, the task moves to Sol: HIGH for
bounded or standard work, XHIGH for complex work, and MAX for exceptional work.
If Sol is unavailable, the primary takes over. Substitutions and limitations
are reported; unavailable models or tools are never assumed to exist.

## Repository

```text
.agents/plugins/       Marketplace entry
plugins/boss-astra/    Plugin manifest, licenses, and skills/boss-astra/SKILL.md
.gitignore
LICENSE
README.md
```

Read the [skill](plugins/boss-astra/skills/boss-astra/SKILL.md) for the routing and delegation rules.

## License

[MIT](LICENSE), with [upstream attribution](plugins/boss-astra/THIRD_PARTY_NOTICES.md).
