---
name: orchestrating-swarms
description: Use when a task should be decomposed across multiple roles, with explicit boundaries, topology, and synthesis.
---

# Orchestrating Swarms

Use this when multiple roles materially improve quality, speed, or coverage.

## Preconditions

- The task has separable concerns.
- The roles can work without clobbering each other.
- There is a clear synthesis point.

## Process

1. Restate the goal.
2. Pick a topology.
3. Assign roles with explicit boundaries.
4. Define expected deliverables per role.
5. Prevent shared-write collisions.
6. Collect outputs.
7. Synthesize into one final result.

## Honesty Rule

If the host cannot actually spawn agents, run the role passes serially and say `runtime: prompt-backed`.
