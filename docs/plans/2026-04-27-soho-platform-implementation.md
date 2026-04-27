# Soho Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use Soho planning, TDD, verification, and orchestration skills while implementing this plan.

**Goal:** Convert Soho from a single prompt-heavy Goose recipe into a layered, testable multi-surface repository.

**Architecture:** Split the system into core recipe, host plugin manifests, methodology skills, orchestration skills, role definitions, schemas, validation scripts, and repository tests.

**Tech Stack:** Markdown, JSON, YAML, Bash, Python 3, unittest

---

### Task 1: Establish repository structure

**Files:**
- Create: `docs/`, `skills/`, `roles/`, `schemas/`, `scripts/`, `tests/`, host plugin directories
- Modify: `.gitignore`, `README.md`, `install.sh`, `soho.yaml`

- [ ] Write the focused repository layout.
- [ ] Replace the monolithic README story with a layered product description.
- [ ] Keep Goose `soho` as the primary recipe entrypoint, opened with `goose recipe open soho`.

### Task 2: Add host adapter surfaces

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `.cursor-plugin/plugin.json`
- Create: `commands/soho.md`, `commands/soho-plan.md`, `commands/soho-swarm.md`

- [ ] Define host metadata for Codex, Claude, and Cursor.
- [ ] Add command entrypoints that route to Soho skills.

### Task 3: Add methodology and orchestration skills

**Files:**
- Create: `skills/*/SKILL.md`

- [ ] Add the Soho entry skill.
- [ ] Add design, planning, TDD, debugging, and verification skills.
- [ ] Add orchestration, topology, synthesis, and subagent-driven skills.

### Task 4: Add role catalog and schemas

**Files:**
- Create: `roles/*.yaml`
- Create: `schemas/role.schema.json`
- Create: `schemas/soho-receipt.schema.json`

- [ ] Define the 16 role contracts.
- [ ] Define JSON-schema style validation targets for roles and receipts.

### Task 5: Add repository validation

**Files:**
- Create: `scripts/validate.py`
- Create: `tests/test_repo.py`
- Create: `Makefile`
- Create: `requirements-dev.txt`

- [ ] Validate manifests, skills, roles, recipe references, and schemas.
- [ ] Run the validation suite and keep it green.
