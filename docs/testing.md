# Testing Soho

## Goals

The test suite validates repository integrity, not host-specific agent behavior.

It checks:

- plugin manifests parse and expose the expected surfaces
- required skills exist and have frontmatter
- required roles exist and match the role schema shape
- the Goose recipe references real sub-recipes
- the receipt schema contains the required fields
- the global installer writes the expected symlinks and recipe files

## Commands

```bash
make validate
make test
make check
```

## Scope

The tests do not claim to prove external host behavior such as:

- whether a specific Codex build auto-discovers the plugin
- whether a given Goose version exposes every orchestration feature
- whether a host can actually spawn subagents

Those are host integration concerns, not repository structure concerns.
