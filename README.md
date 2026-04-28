# SOHO

SOHO is an opinionated agent engineering system that combines:

- **Superpowers-style methodology**: brainstorm before building, write plans before editing, use TDD for behavior changes, debug from root cause, and verify every claim.
- **Ruflo-style orchestration**: choose solo versus swarm deliberately, assign explicit roles, pick a topology, prevent drift, and synthesize outputs into one verified result.

This repository is not a single prompt pretending to be a platform. It is a layered package with:

- a **Goose recipe** opened through Goose's recipe system
- **Codex / Claude / Cursor adapter metadata**
- a **Soho skill library**
- a **role catalog** for orchestrated work
- **schemas** for receipts and role definitions
- a **validation suite** that checks the repo’s own integrity

Public install and validation run on stock Python 3. No separate `PyYAML` install is required.

## What Soho Is

Soho is the product surface. It is meant to feel like one thing:

- the `soho` recipe in Goose
- Soho skills or plugin adapters in Codex / Claude / Cursor, depending on host support
- a disciplined, evidence-first workflow across solo and multi-agent work

Internally, Soho is split into layers so it stays honest:

1. **Core policy**: capability claims, receipts, claim typing, evidence rules
2. **Methodology skills**: design, planning, TDD, debugging, verification
3. **Swarm orchestration**: role selection, topology choice, delegation contracts, synthesis
4. **Host adapters**: Goose, Codex, Claude, Cursor surfaces

## Capability Truth

Read [docs/capability-matrix.md](docs/capability-matrix.md) before assuming a feature is runtime-backed.

The short version:

- **Prompt-backed**: methodology, role contracts, topology guidance, receipt discipline
- **Runtime-backed**: repository validation, host plugin manifests, Goose recipe install, receipt schema validation
- **Host-dependent**: actual parallel agent spawning and orchestration

Soho does not fake receipts. If the host cannot spawn agents, Soho falls back to a serial role-pass workflow and says so explicitly.

## Install

The simplest durable setup is:

1. run the bootstrap script
2. let it clone or update Soho at a stable path
3. let it run the global installer
4. restart the hosts that use file-based discovery

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SoheilOlia/Soho/main/scripts/bootstrap.sh)"
```

By default it uses:

- repo URL: `https://github.com/SoheilOlia/Soho.git`
- install dir: `~/agent-plugins/soho`

You can override the install directory:

```bash
SOHO_INSTALL_DIR=~/tools/soho \
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SoheilOlia/Soho/main/scripts/bootstrap.sh)"
```

The bootstrap script then runs `scripts/install-global.sh`, which wires:

- Goose recipes into `~/.config/goose/recipes`
- Codex skills into `~/.agents/skills/soho`
- a Claude Code local marketplace into `~/.claude/plugins/marketplaces/soho-dev`
- best-effort Cursor local plugin metadata into `~/.cursor/plugins/local/soho`

It then prints the exact host-specific follow-up commands where the host requires one.

Soho is not published to any public host marketplace yet. The installer wires local files on your machine. If a host has a separate marketplace UI, do not expect Soho to appear there until you add the local marketplace or the host re-scans local plugin paths.

### Goose

```bash
./install.sh
```

This validates the repo and installs:

- `soho.yaml`
- all `sub-recipes/*.yaml`

to `~/.config/goose/recipes/`.

Open it with Goose's recipe system:

```bash
goose recipe open soho
```

Goose recipes are not slash commands inside an existing chat. If the Goose command palette only shows built-in commands such as `clear`, `compact`, and `prompt`, that does not mean the recipe failed to install.

### Codex

Codex has a stable machine-global skill discovery path. Soho installs there as:

```text
~/.agents/skills/soho -> /path/to/Soho/skills
```

Then restart Codex and invoke Soho skills by name.

This is a skills install, not a public Codex marketplace install.

### Claude Code

Soho ships a local marketplace at [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). After `./scripts/install-global.sh`, run:

```bash
claude plugin marketplace add ~/.claude/plugins/marketplaces/soho-dev
claude plugin install soho@soho-dev
```

That is the official Claude Code path for a local plugin marketplace.

The installer only creates the local marketplace directory. Claude Code does not install the plugin until you run the two `claude plugin ...` commands. Some Claude surfaces do not expose the interactive `/plugin` slash command; the CLI command is the more reliable install path.

### Cursor

Cursor slash commands are project-local. Install Soho commands into a project with:

```bash
~/agent-plugins/soho/scripts/install-cursor-project.sh /path/to/project
```

Then open or reload that project and type `/soho` in Cursor chat.

The global installer also links best-effort Cursor plugin metadata at `~/.cursor/plugins/local/soho`, but Cursor's documented reusable chat command path is `.cursor/commands/*.md` inside each project. See [docs/install.md](docs/install.md).

## Updating

If Soho is already cloned locally, update it with:

```bash
cd ~/agent-plugins/soho
git pull --ff-only
./scripts/install-global.sh
```

Or rerun the bootstrap command; it handles both clone and update.

## DMG Packaging

On macOS, build a local installer DMG with:

```bash
make dmg
```

The output is written to `dist/Soho-<version>.dmg`. The DMG contains a bundled source snapshot and `Install Soho.command`, which copies Soho into `~/agent-plugins/soho` before running the global installer. See [docs/packaging.md](docs/packaging.md).

## Use

### Goose

Open Soho as a Goose recipe:

```bash
goose recipe open soho
```

### Skill-first hosts

Activate the `using-soho` skill, then describe the work.

## Soho Modes

| Mode | When | Output |
|---|---|---|
| `solo` | tight, local, single-lane work | one agent with full Soho discipline |
| `swarm` | multi-part work with separable concerns | topology + roles + delegation plan + synthesis |
| `recommend` | ambiguous tasks | explicit recommendation plus why |

## Core Rules

- No creative implementation without a design checkpoint.
- No multi-step implementation without a written plan.
- No behavior change without test-first proof.
- No bug fix without root cause evidence.
- No completion claim without fresh verification.
- No swarm theater: if orchestration is not actually runtime-backed in the host, Soho must say so.

## Repository Layout

```text
Soho/
├── soho.yaml
├── sub-recipes/
├── skills/
├── roles/
├── commands/
├── schemas/
├── scripts/
├── tests/
├── docs/
├── .codex-plugin/
├── .claude-plugin/
└── .cursor-plugin/
```

## Validation

Run:

```bash
make check
```

This performs:

- structural validation with `scripts/validate.py`
- repository tests in `tests/test_repo.py`

## Documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/install.md](docs/install.md)
- [docs/capability-matrix.md](docs/capability-matrix.md)
- [docs/testing.md](docs/testing.md)
- [docs/specs/2026-04-27-soho-platform-design.md](docs/specs/2026-04-27-soho-platform-design.md)
- [docs/plans/2026-04-27-soho-platform-implementation.md](docs/plans/2026-04-27-soho-platform-implementation.md)

## Credits

- [Superpowers](https://github.com/obra/superpowers) for the methodology inspiration
- [Ruflo](https://github.com/ruvnet/ruflo) for the orchestration inspiration
- [Goose](https://github.com/block/goose) for the recipe host

## License

MIT
