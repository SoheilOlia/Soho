# Soho Architecture

## Purpose

Soho is a layered agent engineering system that combines process rigor with orchestrated execution.

## Layers

1. **Core policy**
   - receipt contract
   - claim typing
   - runtime truth rules
2. **Methodology**
   - brainstorming
   - planning
   - test-driven development
   - debugging
   - verification
3. **Orchestration**
   - role selection
   - topology selection
   - delegation boundaries
   - synthesis
4. **Host adapters**
   - Goose recipe
   - Codex plugin metadata
   - Claude plugin metadata
   - Cursor plugin metadata

## Execution Model

- **Solo mode**: one agent follows the full Soho methodology.
- **Swarm mode**: the system picks a topology, assigns roles, and synthesizes the outputs back into one answer.
- **Recommend mode**: Soho advises whether solo or swarm is the better fit before proceeding.

## Truth Contract

Soho never conflates:

- documented capability
- prompt-backed behavior
- runtime-backed behavior

Every substantial run should end with a receipt that states what actually happened.
