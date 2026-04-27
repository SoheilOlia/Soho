# Installing Soho Globally

This document separates what is verified from what is merely likely.

## Recommended Clone Path

Use one stable clone path so all hosts point to the same repository:

```bash
git clone https://github.com/SoheilOlia/Soho.git ~/agent-plugins/soho
cd ~/agent-plugins/soho
./scripts/install-global.sh
```

Update later with:

```bash
cd ~/agent-plugins/soho
git pull
./scripts/install-global.sh
```

## Host Matrix

| Host | Install path | Status |
|---|---|---|
| Goose | `~/.config/goose/recipes` | verified |
| Codex | `~/.agents/skills/soho -> repo/skills` | verified |
| Claude Code | local marketplace at `~/.claude/plugins/marketplaces/soho-dev` plus `/plugin install soho@soho-dev` | verified path, manual install command still required |
| Cursor | `~/.cursor/plugins/local/soho` | best-effort local plugin path on this machine |

## What `install-global.sh` Does

1. validates the repository
2. installs Goose recipes
3. installs a Codex global skills symlink
4. installs a Claude Code local marketplace symlink
5. installs a Cursor local plugin symlink

## Claude Code

The official Claude Code marketplace docs support:

- local marketplace directories
- `/plugin marketplace add <path>`
- `/plugin install plugin-name@marketplace-name`

So after the installer runs, use:

```text
/plugin marketplace add ~/.claude/plugins/marketplaces/soho-dev
/plugin install soho@soho-dev
```

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
