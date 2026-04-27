#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SKILLS = {
    "using-soho",
    "brainstorming",
    "writing-plans",
    "test-driven-development",
    "systematic-debugging",
    "verification-before-completion",
    "orchestrating-swarms",
    "selecting-topology",
    "synthesizing-results",
    "subagent-driven-development",
}
REQUIRED_ROLES = {
    "coordinator",
    "coder",
    "tester",
    "reviewer",
    "architect",
    "researcher",
    "security-architect",
    "performance-engineer",
    "documenter",
    "devops-engineer",
    "data-engineer",
    "frontend-specialist",
    "mobile-specialist",
    "ml-ai-specialist",
    "migration-specialist",
    "release-manager",
}


def load_json(path: Path):
    with path.open() as handle:
        return json.load(handle)


def read_text(path: Path):
    return path.read_text()


def load_frontmatter(path: Path):
    text = read_text(path)
    if not text.startswith("---\n"):
        raise ValueError(f"{path} is missing frontmatter")
    _, frontmatter, _ = text.split("---", 2)
    return {
        match.group("key"): match.group("value").strip()
        for match in re.finditer(r"^(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.+?)\s*$", frontmatter, re.MULTILINE)
    }


def has_top_level_key(text: str, key: str):
    pattern = rf"^{re.escape(key)}:\s*"
    return re.search(pattern, text, re.MULTILINE) is not None


def has_yaml_key(text: str, key: str):
    pattern = rf"^{re.escape(key)}:\s*"
    return re.search(pattern, text, re.MULTILINE) is not None


def validate_file_exists(relative_path: str, errors):
    path = REPO_ROOT / relative_path
    if not path.exists():
        errors.append(f"Missing required file: {relative_path}")
    return path


def validate_plugin_manifest(relative_path: str, errors):
    data = load_json(validate_file_exists(relative_path, errors))
    for key in ("name", "version", "description"):
        if key not in data:
            errors.append(f"{relative_path} missing key: {key}")


def validate_claude_marketplace_manifest(errors):
    relative_path = ".claude-plugin/marketplace.json"
    data = load_json(validate_file_exists(relative_path, errors))
    if "description" in data:
        errors.append(f"{relative_path} must put description under metadata.description")
    for key in ("name", "owner", "metadata", "plugins"):
        if key not in data:
            errors.append(f"{relative_path} missing key: {key}")
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict) or "description" not in metadata:
        errors.append(f"{relative_path} missing metadata.description")
    plugins = data.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        errors.append(f"{relative_path} must define at least one plugin")
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"{relative_path} plugins[{index}] must be an object")
            continue
        for key in ("name", "description", "version", "source"):
            if key not in plugin:
                errors.append(f"{relative_path} plugins[{index}] missing key: {key}")


def validate_skill_files(errors):
    skill_dir = REPO_ROOT / "skills"
    found = {path.parent.name for path in skill_dir.glob("*/SKILL.md")}
    missing = REQUIRED_SKILLS - found
    for name in sorted(missing):
        errors.append(f"Missing skill: {name}")
    for skill_path in skill_dir.glob("*/SKILL.md"):
        frontmatter = load_frontmatter(skill_path)
        for key in ("name", "description"):
            if key not in frontmatter:
                errors.append(f"{skill_path.relative_to(REPO_ROOT)} missing frontmatter key: {key}")


def validate_roles(errors):
    role_dir = REPO_ROOT / "roles"
    found = {path.stem for path in role_dir.glob("*.yaml")}
    missing = REQUIRED_ROLES - found
    for name in sorted(missing):
        errors.append(f"Missing role: {name}")
    for role_path in role_dir.glob("*.yaml"):
        role_text = read_text(role_path)
        for key in ("name", "version", "purpose", "when_to_use", "capabilities", "deliverables"):
            if not has_yaml_key(role_text, key):
                errors.append(f"{role_path.relative_to(REPO_ROOT)} missing key: {key}")


def validate_recipe(errors):
    recipe_text = read_text(validate_file_exists("soho.yaml", errors))
    for key in ("version", "title", "description", "instructions"):
        if not has_top_level_key(recipe_text, key):
            errors.append(f"soho.yaml missing key: {key}")
    sub_recipes = [
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
    ]
    for sub_recipe in sub_recipes:
        validate_file_exists(f"sub-recipes/{sub_recipe}", errors)


def validate_schemas(errors):
    receipt_schema = load_json(validate_file_exists("schemas/soho-receipt.schema.json", errors))
    role_schema = load_json(validate_file_exists("schemas/role.schema.json", errors))
    for key in ("required", "properties"):
        if key not in receipt_schema:
            errors.append(f"schemas/soho-receipt.schema.json missing key: {key}")
        if key not in role_schema:
            errors.append(f"schemas/role.schema.json missing key: {key}")


def validate_docs(errors):
    for doc in (
        "docs/architecture.md",
        "docs/install.md",
        "docs/packaging.md",
        "docs/capability-matrix.md",
        "docs/testing.md",
        "docs/specs/2026-04-27-soho-platform-design.md",
        "docs/plans/2026-04-27-soho-platform-implementation.md",
        "docs/plans/2026-04-27-soho-dmg-packaging.md",
    ):
        validate_file_exists(doc, errors)


def validate_commands(errors):
    for command in (
        "commands/soho.md",
        "commands/soho-plan.md",
        "commands/soho-swarm.md",
    ):
        validate_file_exists(command, errors)


def validate_scripts(errors):
    for script in (
        "install.sh",
        "scripts/bootstrap.sh",
        "scripts/build-dmg.sh",
        "scripts/install-global.sh",
        "scripts/validate.py",
    ):
        validate_file_exists(script, errors)


def run_validation():
    errors = []
    validate_plugin_manifest(".codex-plugin/plugin.json", errors)
    validate_plugin_manifest(".claude-plugin/plugin.json", errors)
    validate_plugin_manifest(".cursor-plugin/plugin.json", errors)
    validate_claude_marketplace_manifest(errors)
    validate_skill_files(errors)
    validate_roles(errors)
    validate_recipe(errors)
    validate_schemas(errors)
    validate_docs(errors)
    validate_commands(errors)
    validate_scripts(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Soho repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(run_validation())
