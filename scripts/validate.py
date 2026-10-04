"""Validate the portable boss-astra instruction package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:  # pragma: no cover - reported by the CLI when unavailable
    yaml = None


REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "docs/evaluation.md",
    "plugin.json",
    ".agents/plugins/marketplace.json",
    "skills/boss-astra/SKILL.md",
    "skills/boss-astra/agents/openai.yaml",
    "skills/boss-astra/LICENSE",
    "skills/boss-astra/THIRD_PARTY_NOTICES.md",
)
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(\s*(<[^>]+>|[^)\s]+)")


def _read_text(root: Path, relative: str, errors: list[str]) -> str | None:
    path = root / relative
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{relative}: cannot read UTF-8 text ({exc})")
        return None


def _read_json(root: Path, relative: str, errors: list[str]) -> object | None:
    raw = _read_text(root, relative, errors)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"{relative}:{exc.lineno}: malformed JSON: {exc.msg}")
        return None


def _mapping(value: object, relative: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{relative}: expected a YAML/JSON mapping")
        return {}
    return value


def _without_fenced_code(markdown: str) -> str:
    kept: list[str] = []
    fence: tuple[str, int] | None = None
    for line in markdown.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence is None:
            if match:
                fence = (match.group(1)[0], len(match.group(1)))
            else:
                kept.append(line)
        elif match and match.group(1)[0] == fence[0] and len(match.group(1)) >= fence[1]:
            fence = None
    return re.sub(r"(`+).*?\1", "", "\n".join(kept))


def _validate_markdown_links(root: Path, errors: list[str]) -> None:
    root = root.resolve()
    for relative in REQUIRED_FILES:
        if not relative.lower().endswith((".md", ".markdown")):
            continue
        raw = _read_text(root, relative, errors)
        if raw is None:
            continue
        for match in LINK.finditer(_without_fenced_code(raw)):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target_path = unquote(parsed.path)
            if Path(target_path).suffix.lower() not in (".md", ".markdown"):
                continue
            destination = (root / relative).parent / target_path
            try:
                resolved = destination.resolve()
                resolved.relative_to(root)
            except (OSError, ValueError):
                errors.append(f"{relative}: Markdown link escapes repository: {target}")
                continue
            if not resolved.is_file():
                errors.append(f"{relative}: broken Markdown link: {target}")


def validate_repository(root: Path) -> list[str]:
    """Return file-specific validation errors for a package root."""
    root = Path(root).resolve()
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"{relative}: required file is missing")
            continue
        if path.stat().st_size == 0:
            errors.append(f"{relative}: required file is empty")

    for notice in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        bundled = root / "skills" / "boss-astra" / notice
        original = root / notice
        if bundled.is_file() and original.is_file() and bundled.read_bytes() != original.read_bytes():
            errors.append(f"skills/boss-astra/{notice}: must match the root notice for standalone distribution")

    plugin_rel = "plugin.json"
    plugin = _read_json(root, plugin_rel, errors)
    plugin_data = _mapping(plugin, plugin_rel, errors) if plugin is not None else {}
    plugin_name = plugin_data.get("name")
    if not isinstance(plugin_name, str) or not SLUG.fullmatch(plugin_name):
        errors.append(f"{plugin_rel}: name must be a lowercase hyphenated string")
        plugin_name = None
    version = plugin_data.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        errors.append(f"{plugin_rel}: version must use semantic x.y.z form")
    if not isinstance(plugin_data.get("description"), str) or not plugin_data["description"].strip():
        errors.append(f"{plugin_rel}: description must be a nonempty string")

    market_rel = ".agents/plugins/marketplace.json"
    marketplace = _read_json(root, market_rel, errors)
    market_data = _mapping(marketplace, market_rel, errors) if marketplace is not None else {}
    if plugin_name and market_data.get("name") != plugin_name:
        errors.append(f"{market_rel}: marketplace name must match plugin.json name {plugin_name!r}")
    entries = market_data.get("plugins")
    if not isinstance(entries, list):
        errors.append(f"{market_rel}: plugins must be a list")
        entries = []
    matches = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == plugin_name]
    if len(matches) != 1:
        errors.append(f"{market_rel}: expected exactly one plugin entry matching plugin.json name")
    for entry in matches[:1]:
        source = entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "local":
            errors.append(f"{market_rel}: plugin source must be a local source mapping")
            continue
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path.startswith("./") or "\\" in source_path:
            errors.append(f"{market_rel}: local source path must start with ./ and use forward slashes")
            continue
        parts = Path(source_path[2:]).parts
        if ".." in parts:
            errors.append(f"{market_rel}: local source path must not contain ..")
            continue
        try:
            resolved = (root / source_path[2:]).resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            errors.append(f"{market_rel}: local source path must resolve within repository")
            continue
        source_manifest = resolved / "plugin.json"
        if not source_manifest.is_file():
            errors.append(f"{market_rel}: local source path does not resolve to a plugin")
        elif resolved != root:
            try:
                source_data = json.loads(source_manifest.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                errors.append(f"{market_rel}: local source plugin.json is unreadable or malformed")
            else:
                if not isinstance(source_data, dict) or source_data.get("name") != plugin_name:
                    errors.append(f"{market_rel}: local source resolves to a different plugin")
        policy = entry.get("policy")
        if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
            errors.append(f"{market_rel}: plugin policy must be AVAILABLE and ON_INSTALL")
        if entry.get("category") != "Productivity":
            errors.append(f"{market_rel}: plugin category must be Productivity")

    skill_rel = "skills/boss-astra/SKILL.md"
    skill_text = _read_text(root, skill_rel, errors)
    if skill_text is not None:
        front = re.match(r"\A---[ \t]*\n(.*?)^---[ \t]*(?:\n|$)", skill_text, re.DOTALL | re.MULTILINE)
        if not front:
            errors.append(f"{skill_rel}: missing YAML frontmatter")
        elif yaml is None:
            errors.append(f"{skill_rel}: PyYAML is required to validate frontmatter")
        else:
            try:
                metadata = yaml.safe_load(front.group(1))
            except yaml.YAMLError as exc:
                errors.append(f"{skill_rel}: malformed YAML frontmatter: {exc}")
            else:
                metadata = _mapping(metadata, skill_rel, errors)
                name = metadata.get("name")
                if not isinstance(name, str) or not SLUG.fullmatch(name) or name != Path(skill_rel).parent.name:
                    errors.append(f"{skill_rel}: name must be a lowercase hyphenated string matching its folder")
                description = metadata.get("description")
                if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                    errors.append(f"{skill_rel}: description must be nonempty and at most 1024 characters")
        if front and not skill_text[front.end():].strip():
            errors.append(f"{skill_rel}: instruction body must be nonempty")

    ui_rel = "skills/boss-astra/agents/openai.yaml"
    ui_text = _read_text(root, ui_rel, errors)
    if ui_text is not None:
        if yaml is None:
            errors.append(f"{ui_rel}: PyYAML is required to validate metadata")
        else:
            try:
                ui = yaml.safe_load(ui_text)
            except yaml.YAMLError as exc:
                errors.append(f"{ui_rel}: malformed YAML: {exc}")
            else:
                ui = _mapping(ui, ui_rel, errors)
                interface = ui.get("interface")
                if not isinstance(interface, dict):
                    errors.append(f"{ui_rel}: interface must be a mapping")
                    interface = {}
                if not isinstance(interface.get("display_name"), str) or not interface["display_name"].strip():
                    errors.append(f"{ui_rel}: interface.display_name must be a nonempty string")
                short = interface.get("short_description")
                if not isinstance(short, str) or not 25 <= len(short) <= 64:
                    errors.append(f"{ui_rel}: interface.short_description must be 25-64 characters")
                prompt = interface.get("default_prompt")
                if not isinstance(prompt, str) or "$boss-astra" not in prompt:
                    errors.append(f"{ui_rel}: interface.default_prompt must reference $boss-astra")
                policy = ui.get("policy")
                if not isinstance(policy, dict) or not isinstance(policy.get("allow_implicit_invocation"), bool):
                    errors.append(f"{ui_rel}: policy.allow_implicit_invocation must be a boolean")

    _validate_markdown_links(root, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
