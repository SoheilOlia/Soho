---
name: brainstorming
description: Use before creative implementation work to clarify the goal, explore approaches, and lock the design before editing files.
---

# Brainstorming

Use this before building a feature, changing behavior, or introducing new structure.

## Process

1. Inspect the current project context.
2. Clarify the real goal and constraints.
3. Offer 2-3 approaches when there is real design choice.
4. Recommend one approach and explain why.
5. Write the design to `$SOHO_DOCS_DIR/specs/` when set, otherwise `docs/specs/` in a real project.
6. Get approval before implementation.

## Guardrails

- Do not code through ambiguity.
- Prefer simpler boundaries and fewer moving parts.
- In existing repos, preserve established patterns unless the task requires a better seam.
- If there is no safe project docs directory, keep the design inline and say it was not written to disk.
