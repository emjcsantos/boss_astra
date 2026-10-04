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
