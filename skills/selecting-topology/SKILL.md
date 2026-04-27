---
name: selecting-topology
description: Use when Soho swarm mode is active and the task needs a justified topology choice.
---

# Selecting Topology

Choose the topology that best matches the work:

- `hierarchical`: implementation, coordination, anti-drift control
- `mesh`: exploration, comparison, open-ended research
- `ring`: ordered pipeline stages
- `star`: parallel independent workstreams

## Rule of Thumb

Default to `hierarchical` for coding tasks unless there is a strong reason not to.

## Output

State:

- chosen topology
- why it fits
- what failure mode it avoids
