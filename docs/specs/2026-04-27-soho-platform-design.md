# Soho Platform Design

## Problem

The original Soho repo was a single Goose recipe that narrated a merged Superpowers-plus-Ruflo identity without providing the supporting structure, receipts, tests, or host adapter surfaces to make that claim trustworthy.

## Goal

Turn Soho into a real layered system that:

- preserves Superpowers-style methodology
- preserves Ruflo-style orchestration concepts
- exposes one Soho product surface across hosts
- distinguishes prompt-backed behavior from runtime-backed behavior
- validates its own repository structure with tests

## Architecture

Soho will use a layered architecture:

1. core policy and truth contracts
2. methodology skills
3. orchestration skills and role catalog
4. host adapters and recipes
5. validation suite

## Constraints

- do not fake runtime orchestration if the host cannot provide it
- keep the repo installation story simple
- prefer small, focused files over another monolithic prompt

## Success Criteria

- Goose recipe remains usable
- Soho skills exist as discrete files
- role catalog exists as discrete YAML definitions
- plugin manifests exist for Codex, Claude, and Cursor
- validation suite passes
- documentation explains what is real versus host-dependent
