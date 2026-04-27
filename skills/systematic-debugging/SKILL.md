---
name: systematic-debugging
description: Use when a bug, broken test, or unexpected result needs root-cause investigation before any fix is attempted.
---

# Systematic Debugging

No fix without root cause evidence.

## Process

1. Reproduce the failure consistently.
2. Read the actual error or mismatch carefully.
3. Trace the failing path through the system.
4. Compare against a known-good path or reference.
5. Form a single hypothesis.
6. Test the hypothesis with the smallest useful change.
7. Only then implement the real fix.

## Anti-Patterns

- patching symptoms
- changing multiple variables at once
- assuming the latest touched file is the source of the bug
