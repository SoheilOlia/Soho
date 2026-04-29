import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

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

    def test_example_receipt_matches_schema_required_fields(self):
        schema = json.loads((REPO_ROOT / "schemas" / "soho-receipt.schema.json").read_text())
        receipt = json.loads((REPO_ROOT / "docs" / "example-receipt.json").read_text())
        for field in schema["required"]:
            self.assertIn(field, receipt)
        self.assertIn(receipt["host"], schema["properties"]["host"]["enum"])
        self.assertIn(receipt["mode"], schema["properties"]["mode"]["enum"])
        self.assertIn(receipt["runtime"], schema["properties"]["runtime"]["enum"])
        self.assertIn(receipt["confidence"], schema["properties"]["confidence"]["enum"])

    def test_recipe_references_real_sub_recipes(self):
        recipe_text = (REPO_ROOT / "soho.yaml").read_text()
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
            self.assertIn(name, recipe_text)
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

    def test_cursor_project_install_script_writes_project_commands(self):
        with tempfile.TemporaryDirectory() as temp_project:
            subprocess.run(
                ["bash", "scripts/install-cursor-project.sh", temp_project],
                cwd=REPO_ROOT,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            commands_dir = Path(temp_project) / ".cursor" / "commands"
            for name in ("soho.md", "soho-plan.md", "soho-swarm.md"):
                installed = commands_dir / name
                self.assertTrue(installed.exists())
                self.assertEqual(installed.read_text(), (REPO_ROOT / "commands" / name).read_text())

    def test_public_skill_cursor_commands_match_project_commands(self):
        public_cursor_dir = REPO_ROOT / "skills" / "using-soho" / "cursor"
        for name in ("soho.md", "soho-plan.md", "soho-swarm.md"):
            self.assertTrue((public_cursor_dir / name).exists())
            self.assertEqual((public_cursor_dir / name).read_text(), (REPO_ROOT / "commands" / name).read_text())

    def test_mirror_check_script_can_validate_explicit_mirror(self):
        with tempfile.TemporaryDirectory() as temp_root:
            mirror = Path(temp_root) / "skills"
            shutil.copytree(REPO_ROOT / "skills", mirror)
            subprocess.run(
                ["bash", "scripts/check-skills-mirror.sh"],
                cwd=REPO_ROOT,
                env={**os.environ, "SOHO_SKILLS_MIRROR_DIR": str(mirror)},
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

    def test_mirror_check_script_fails_on_drift(self):
        with tempfile.TemporaryDirectory() as temp_root:
            mirror = Path(temp_root) / "skills"
            shutil.copytree(REPO_ROOT / "skills", mirror)
            (mirror / "using-soho" / "SKILL.md").write_text("drift")

            result = subprocess.run(
                ["bash", "scripts/check-skills-mirror.sh"],
                cwd=REPO_ROOT,
                env={**os.environ, "SOHO_SKILLS_MIRROR_DIR": str(mirror)},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)

    def test_canonical_local_skills_mirror_matches_when_present(self):
        mirror = Path.home() / "skills" / "soho" / "skills"
        if not mirror.exists():
            self.skipTest(f"canonical mirror not present: {mirror}")

        subprocess.run(
            ["bash", "scripts/check-skills-mirror.sh"],
            cwd=REPO_ROOT,
            env={**os.environ, "SOHO_SKILLS_MIRROR_DIR": str(mirror)},
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def test_goose_docs_do_not_claim_slash_command_install(self):
        checked_files = (
            REPO_ROOT / "README.md",
            REPO_ROOT / "docs" / "install.md",
            REPO_ROOT / "docs" / "capability-matrix.md",
            REPO_ROOT / "install.sh",
            REPO_ROOT / "scripts" / "install-global.sh",
        )
        for path in checked_files:
            text = path.read_text()
            self.assertNotIn("run /soho", text, path)
            self.assertNotIn("Goose `/soho`", text, path)

        self.assertIn("goose recipe open soho", (REPO_ROOT / "README.md").read_text())
        self.assertIn("goose recipe open soho", (REPO_ROOT / "docs" / "install.md").read_text())

    def test_claude_docs_prefer_cli_plugin_commands(self):
        checked_files = (
            REPO_ROOT / "README.md",
            REPO_ROOT / "docs" / "install.md",
            REPO_ROOT / "docs" / "capability-matrix.md",
            REPO_ROOT / "scripts" / "install-global.sh",
        )
        for path in checked_files:
            text = path.read_text()
            self.assertNotIn("/plugin marketplace add", text, path)
            self.assertNotIn("/plugin install", text, path)

        install_text = (REPO_ROOT / "docs" / "install.md").read_text()
        self.assertIn("claude plugin marketplace add", install_text)
        self.assertIn("claude plugin install", install_text)

    def test_cursor_docs_use_project_commands_not_global_plugin_claim(self):
        install_text = (REPO_ROOT / "docs" / "install.md").read_text()
        readme_text = (REPO_ROOT / "README.md").read_text()
        self.assertIn("scripts/install-cursor-project.sh", install_text)
        self.assertIn(".cursor/commands/soho.md", install_text)
        self.assertIn("Cursor slash commands are project-local", readme_text)

    def test_dmg_packaging_script_is_executable_and_documented(self):
        script = REPO_ROOT / "scripts" / "build-dmg.sh"
        self.assertTrue(script.exists())
        self.assertTrue(os.access(script, os.X_OK))

        mirror_script = REPO_ROOT / "scripts" / "check-skills-mirror.sh"
        self.assertTrue(mirror_script.exists())
        self.assertTrue(os.access(mirror_script, os.X_OK))

        makefile_text = (REPO_ROOT / "Makefile").read_text()
        self.assertIn("dmg:", makefile_text)
        self.assertIn("scripts/build-dmg.sh", makefile_text)
        self.assertIn("mirror-check:", makefile_text)

        packaging_text = (REPO_ROOT / "docs" / "packaging.md").read_text()
        self.assertIn("make dmg", packaging_text)
        self.assertIn("Install Soho.command", packaging_text)

    def test_dmg_packaging_dry_run_stages_installer(self):
        with tempfile.TemporaryDirectory() as temp_root:
            dist_dir = Path(temp_root) / "dist"
            build_dir = Path(temp_root) / "build"
            subprocess.run(
                ["bash", "scripts/build-dmg.sh"],
                cwd=REPO_ROOT,
                env={
                    **os.environ,
                    "DIST_DIR": str(dist_dir),
                    "BUILD_DIR": str(build_dir),
                    "SOHO_DMG_DRY_RUN": "1",
                },
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            stage_dir = build_dir / "stage"
            installer = stage_dir / "Install Soho.command"
            readme = stage_dir / "README.txt"
            source_dir = stage_dir / "Soho"

            self.assertTrue(installer.exists())
            self.assertTrue(os.access(installer, os.X_OK))
            self.assertTrue(readme.exists())
            self.assertTrue((source_dir / "scripts" / "install-global.sh").exists())
            self.assertFalse((source_dir / ".git").exists())

            installer_text = installer.read_text()
            self.assertIn("SOHO_INSTALL_DIR", installer_text)
            self.assertIn("rsync -a", installer_text)
            self.assertIn("./scripts/install-global.sh", installer_text)
            self.assertIn("claude plugin marketplace add", installer_text)
            self.assertIn("goose recipe open soho", installer_text)

    def test_bootstrap_script_clones_then_updates(self):
        with tempfile.TemporaryDirectory() as temp_root:
            remote_source = Path(temp_root) / "remote-source"
            shutil.copytree(
                REPO_ROOT,
                remote_source,
                ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"),
            )
            subprocess.run(
                ["git", "init", "-b", "main"],
                cwd=remote_source,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            subprocess.run(
                ["git", "add", "."],
                cwd=remote_source,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            subprocess.run(
                ["git", "-c", "user.name=Test User", "-c", "user.email=test@example.com", "commit", "-m", "initial"],
                cwd=remote_source,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            install_dir = Path(temp_root) / "agent-plugins" / "soho"
            goose_dir = Path(temp_root) / "goose" / "recipes"
            codex_dir = Path(temp_root) / "agents" / "skills"
            claude_dir = Path(temp_root) / "claude" / "plugins" / "marketplaces"
            cursor_dir = Path(temp_root) / "cursor" / "plugins" / "local"
            env = {
                **os.environ,
                "SOHO_REPO_URL": str(remote_source),
                "SOHO_INSTALL_DIR": str(install_dir),
                "GOOSE_RECIPE_DIR": str(goose_dir),
                "CODEX_SKILLS_DIR": str(codex_dir),
                "CLAUDE_MARKETPLACES_DIR": str(claude_dir),
                "CURSOR_LOCAL_PLUGINS_DIR": str(cursor_dir),
            }

            subprocess.run(
                ["bash", str(REPO_ROOT / "scripts" / "bootstrap.sh")],
                cwd=REPO_ROOT,
                env=env,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertTrue((install_dir / "scripts" / "install-global.sh").exists())
            self.assertTrue((goose_dir / "soho.yaml").exists())

            subprocess.run(
                ["bash", str(REPO_ROOT / "scripts" / "bootstrap.sh")],
                cwd=REPO_ROOT,
                env=env,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertTrue((codex_dir / "soho").is_symlink())


if __name__ == "__main__":
    unittest.main()
