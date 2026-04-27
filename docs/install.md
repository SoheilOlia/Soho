# Installing Soho Globally

This document separates what is verified from what is merely likely.

## Recommended Clone Path

Use one stable clone path so all hosts point to the same repository:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SoheilOlia/Soho/main/scripts/bootstrap.sh)"
```

The bootstrap script:

1. clones Soho if the target directory does not exist
2. fast-forwards the existing clone if it does exist
3. runs `scripts/install-global.sh`

By default it uses:

```text
SOHO_REPO_URL=https://github.com/SoheilOlia/Soho.git
SOHO_INSTALL_DIR=~/agent-plugins/soho
```

Override example:

```bash
SOHO_INSTALL_DIR=~/tools/soho \
bash -c "$(curl -fsSL https://raw.githubusercontent.com/SoheilOlia/Soho/main/scripts/bootstrap.sh)"
```

Manual update later with:

```bash
cd ~/agent-plugins/soho
git pull --ff-only
./scripts/install-global.sh
```

## Host Matrix

| Host | Install path | Status |
|---|---|---|
| Goose | `~/.config/goose/recipes`, opened with `goose recipe open soho` | verified recipe install |
| Codex | `~/.agents/skills/soho -> repo/skills` | verified |
| Claude Code | local marketplace at `~/.claude/plugins/marketplaces/soho-dev` plus `claude plugin install soho@soho-dev` | verified path, manual install command still required |
| Cursor | `~/.cursor/plugins/local/soho` | best-effort local plugin path on this machine |

Soho is not currently published to a public marketplace. These are local installs. Marketplace UIs will not show Soho unless the host explicitly supports adding local marketplaces or scanning local plugin paths.

## What `install-global.sh` Does

1. validates the repository
2. installs Goose recipes
3. installs a Codex global skills symlink
4. installs a Claude Code local marketplace symlink
5. installs a Cursor local plugin symlink

## Goose

The installer copies `soho.yaml` and `sub-recipes/*.yaml` into Goose's recipe directory:

```text
~/.config/goose/recipes
```

Open Soho with:

```bash
goose recipe open soho
```

Do not expect `/soho` to appear in the Goose slash-command menu. Goose recipes are launched through the recipe system, not as custom slash commands inside an existing chat.

## Existing Directory Case

If `~/agent-plugins/soho` already exists, do not run `git clone` again in that folder. Either:

```bash
cd ~/agent-plugins/soho
git pull --ff-only
./scripts/install-global.sh
```

or rerun the bootstrap command, which handles this automatically.

## Claude Code

Claude Code supports plugin management through the `claude plugin` CLI:

- local marketplace directories
- `claude plugin marketplace add <path>`
- `claude plugin install plugin-name@marketplace-name`

So after the installer runs, use:

```bash
claude plugin marketplace add ~/.claude/plugins/marketplaces/soho-dev
claude plugin install soho@soho-dev
```

If Soho does not appear in Claude Code before those commands, that is expected. The installer creates the local marketplace path; Claude Code still has to add that marketplace and install from it.

Some Claude surfaces do not expose the interactive `/plugin` slash command. Use the CLI form above when `/plugin` is unavailable.

If you are actively developing Soho, you can also test it directly with:

```bash
claude --plugin-dir ~/agent-plugins/soho
```

That is a development path, not the normal machine-global install path.

## Codex

Codex skill discovery works well with a namespaced skills symlink:

```text
~/.agents/skills/soho -> ~/agent-plugins/soho/skills
```

This is the same general pattern used by Superpowers for Codex.

Codex discovers Soho as skills after restart. This does not imply Soho will appear in a separate public marketplace or generic local-plugin UI.

## Cursor

Cursor on this machine has a local plugin directory at:

```text
~/.cursor/plugins/local
```

The installer places Soho at:

```text
~/.cursor/plugins/local/soho
```

Confidence is lower here than Goose, Codex, and Claude Code because I do not yet have a strong official Cursor plugin-install reference comparable to Claude’s marketplace docs.

## Outside Block

Nothing in Soho is Block-internal. It is a public GitHub repository with local files, Markdown skills, YAML recipes, JSON manifests, and Python validation scripts. Anyone with:

- Git
- Python 3
- a supported host

can clone it and install it locally.
