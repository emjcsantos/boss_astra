import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import validate_repository


class ValidateRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write("README.md", "# Package\n")
        self.write("LICENSE", "License text\n")
        self.write("THIRD_PARTY_NOTICES.md", "No third-party material.\n")
        self.write("skills/boss-astra/LICENSE", "License text\n")
        self.write("skills/boss-astra/THIRD_PARTY_NOTICES.md", "No third-party material.\n")
        self.write("CONTRIBUTING.md", "Contribution guidance.\n")
        self.write("AGENTS.md", "Repository guidance.\n")
        self.write("docs/evaluation.md", "Behavioral scenarios.\n")
        self.write(
            "plugin.json",
            json.dumps({"name": "boss-astra", "version": "0.1.0", "description": "A reusable advisor."}),
        )
        self.write(
            ".agents/plugins/marketplace.json",
            json.dumps(
                {
                    "name": "boss-astra",
                    "plugins": [
                        {
                            "name": "boss-astra",
                            "source": {"source": "local", "path": "./"},
                            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                            "category": "Productivity",
                        }
                    ],
                }
            ),
        )
        self.write(
            "skills/boss-astra/SKILL.md",
            "---\nname: boss-astra\ndescription: Helps turn goals into useful plans.\n---\n\n"
            "Use this skill to clarify a goal and identify a practical next step.\n",
        )
        self.write(
            "skills/boss-astra/agents/openai.yaml",
            "interface:\n"
            "  display_name: Boss Astra\n"
            "  short_description: Turns goals into clear action steps.\n"
            "  default_prompt: Use $boss-astra to help me plan.\n"
            "policy:\n"
            "  allow_implicit_invocation: false\n",
        )

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def errors(self):
        return validate_repository(self.root)

    def test_accepts_a_valid_portable_package(self):
        self.assertEqual([], self.errors())

    def test_requires_standalone_license_notices(self):
        for notice in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
            relative = f"skills/boss-astra/{notice}"
            content = (self.root / relative).read_text(encoding="utf-8")
            with self.subTest(notice=notice):
                (self.root / relative).unlink()
                self.assertTrue(any(f"{relative}: required file is missing" in error for error in self.errors()))
            self.write(relative, content)

    def test_rejects_drifting_standalone_notices(self):
        self.write("skills/boss-astra/THIRD_PARTY_NOTICES.md", "Incomplete notices.\n")
        self.assertTrue(any("must match the root notice" in error for error in self.errors()))

    def test_reports_malformed_skill_frontmatter_yaml(self):
        self.write("skills/boss-astra/SKILL.md", "---\nname: [\n---\nInstructions.\n")
        self.assertTrue(any("malformed YAML frontmatter" in error for error in self.errors()))

    def test_requires_skill_frontmatter_to_be_a_mapping(self):
        self.write("skills/boss-astra/SKILL.md", "---\n---\nInstructions.\n")
        self.assertTrue(any("expected a YAML/JSON mapping" in error for error in self.errors()))

    def test_does_not_treat_inline_dashes_as_a_frontmatter_boundary(self):
        self.write(
            "skills/boss-astra/SKILL.md",
            "---\nname: boss-astra\ndescription: Handle a---b dependencies.\n---\nInstructions.\n",
        )
        self.assertEqual([], self.errors())

    def test_reports_malformed_plugin_json(self):
        self.write("plugin.json", "{\n")
        self.assertTrue(any("plugin.json:1: malformed JSON" in error or "plugin.json:2: malformed JSON" in error for error in self.errors()))

    def test_reports_a_missing_skill_file(self):
        (self.root / "skills/boss-astra/SKILL.md").unlink()
        self.assertTrue(any("skills/boss-astra/SKILL.md: required file is missing" in error for error in self.errors()))

    def test_requires_the_ui_prompt_to_reference_the_skill(self):
        self.write(
            "skills/boss-astra/agents/openai.yaml",
            "interface:\n  display_name: Boss Astra\n"
            "  short_description: Turns goals into clear action steps.\n"
            "  default_prompt: Help me plan.\n"
            "policy:\n  allow_implicit_invocation: false\n",
        )
        self.assertTrue(any("default_prompt must reference $boss-astra" in error for error in self.errors()))

    def test_requires_marketplace_and_plugin_names_to_match(self):
        self.write(
            "plugin.json",
            json.dumps({"name": "other-plugin", "version": "0.1.0", "description": "A reusable advisor."}),
        )
        errors = self.errors()
        self.assertTrue(any("marketplace name must match plugin.json name" in error for error in errors))
        self.assertTrue(any("plugin entry matching plugin.json name" in error for error in errors))

    def test_rejects_a_local_source_that_escapes_the_repository(self):
        marketplace = json.loads((self.root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        marketplace["plugins"][0]["source"]["path"] = "./../outside"
        self.write(".agents/plugins/marketplace.json", json.dumps(marketplace))
        self.assertTrue(any("local source path must not contain .." in error for error in self.errors()))

    def test_reports_broken_relative_markdown_links(self):
        self.write("README.md", "# Package\n\n[Guide](docs/missing.md)\n")
        self.assertTrue(any("README.md: broken Markdown link: docs/missing.md" in error for error in self.errors()))

    def test_ignores_markdown_links_inside_fenced_code(self):
        self.write("README.md", "# Package\n\n```md\n[Guide](missing.md)\n```\n")
        self.assertEqual([], self.errors())


if __name__ == "__main__":
    unittest.main()
