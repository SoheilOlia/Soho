import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate import REQUIRED_ROLES, REQUIRED_SKILLS, REPO_ROOT, run_validation


class RepoStructureTests(unittest.TestCase):
    def test_validation_script_passes(self):
        self.assertEqual(run_validation(), 0)

    def test_expected_skills_exist(self):
        found = {path.parent.name for path in (REPO_ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(found, REQUIRED_SKILLS)

    def test_expected_roles_exist(self):
        found = {path.stem for path in (REPO_ROOT / "roles").glob("*.yaml")}
        self.assertEqual(found, REQUIRED_ROLES)

    def test_receipt_schema_required_fields(self):
        schema_path = REPO_ROOT / "schemas" / "soho-receipt.schema.json"
        schema = json.loads(schema_path.read_text())
        required = set(schema["required"])
        for field in ("generated_at", "host", "mode", "runtime", "task_summary", "evidence", "outputs", "confidence"):
            self.assertIn(field, required)

    def test_recipe_references_real_sub_recipes(self):
        recipe = yaml.safe_load((REPO_ROOT / "soho.yaml").read_text())
        instructions = recipe["instructions"]
        for name in (
            "architecture-design.yaml",
            "code-review.yaml",
            "documentation.yaml",
            "migration.yaml",
            "performance-optimization.yaml",
            "project-setup.yaml",
            "release-management.yaml",
            "security-audit.yaml",
            "sparc-workflow.yaml",
            "solo-execution.yaml",
            "swarm-orchestration.yaml",
            "test-suite.yaml",
        ):
            self.assertIn(name, instructions)
            self.assertTrue((REPO_ROOT / "sub-recipes" / name).exists())

    def test_install_script_installs_goose_recipe_files(self):
        with tempfile.TemporaryDirectory() as temp_home:
            subprocess.run(
                ["bash", "install.sh"],
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": temp_home},
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            recipe_root = Path(temp_home) / ".config" / "goose" / "recipes"
            self.assertTrue((recipe_root / "soho.yaml").exists())
            self.assertTrue((recipe_root / "sub-recipes" / "swarm-orchestration.yaml").exists())

    def test_global_install_script_wires_all_supported_paths(self):
        with tempfile.TemporaryDirectory() as temp_root:
            goose_dir = Path(temp_root) / "goose" / "recipes"
            codex_dir = Path(temp_root) / "agents" / "skills"
            claude_dir = Path(temp_root) / "claude" / "plugins" / "marketplaces"
            cursor_dir = Path(temp_root) / "cursor" / "plugins" / "local"
            subprocess.run(
                ["bash", "scripts/install-global.sh"],
                cwd=REPO_ROOT,
                env={
                    **os.environ,
                    "GOOSE_RECIPE_DIR": str(goose_dir),
                    "CODEX_SKILLS_DIR": str(codex_dir),
                    "CLAUDE_MARKETPLACES_DIR": str(claude_dir),
                    "CURSOR_LOCAL_PLUGINS_DIR": str(cursor_dir),
                },
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertTrue((goose_dir / "soho.yaml").exists())
            self.assertTrue((goose_dir / "sub-recipes" / "solo-execution.yaml").exists())
            self.assertTrue((codex_dir / "soho").is_symlink())
            self.assertEqual((codex_dir / "soho").resolve(), (REPO_ROOT / "skills").resolve())
            self.assertTrue((claude_dir / "soho-dev").is_symlink())
            self.assertEqual((claude_dir / "soho-dev").resolve(), REPO_ROOT.resolve())
            self.assertTrue((cursor_dir / "soho").is_symlink())
            self.assertEqual((cursor_dir / "soho").resolve(), REPO_ROOT.resolve())


if __name__ == "__main__":
    unittest.main()
