---
name: subagent-driven-development
description: Use when Soho should execute a plan through delegated tasks with role boundaries and review checkpoints.
---

# Subagent-Driven Development

Use this when the host supports delegation, or when a serial role-pass simulation is still useful.

## Process

1. Start from a written plan.
2. Dispatch one bounded task at a time.
3. Give each task:
   - exact scope
   - files or surfaces it owns
   - verification expectation
4. Review outputs before moving on.
5. Synthesize results continuously, not just at the end.

## Guardrails

- Never let two workers edit the same file without coordination.
- Keep delegated tasks concrete and narrow.
- If the host lacks real delegation, say so and simulate the role passes serially.
