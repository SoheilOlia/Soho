---
name: writing-plans
description: Use when a task has multiple implementation steps and needs an exact plan before code changes.
---

# Writing Plans

Use this when implementation spans more than a trivial edit.

## Plan Requirements

- Save the plan to `$SOHO_DOCS_DIR/plans/` when set, otherwise `docs/plans/` in a real project.
- Use exact file paths.
- Break work into small executable steps.
- Include testing and verification steps.
- Avoid placeholders like `TODO`, `later`, or `add tests`.
- If there is no safe project docs directory, keep the plan inline and say it was not written to disk.

## Minimum Structure

- goal
- architecture summary
- files to create or modify
- implementation steps
- test steps
- verification steps

## Rule

If you cannot write the plan cleanly, the design is still muddy.
