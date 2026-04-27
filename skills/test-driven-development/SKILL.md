---
name: test-driven-development
description: Use for behavior changes, new features, bug fixes, and refactors that should be proven with test-first execution.
---

# Test-Driven Development

No production behavior change without a failing test first.

## Cycle

1. Write one failing test for one behavior.
2. Run it and confirm it fails for the expected reason.
3. Write the smallest implementation that makes it pass.
4. Run the test again.
5. Refactor only after green.

## Guardrails

- If the test passes immediately, you are not proving new behavior.
- If the failure is unrelated, fix the test until it fails correctly.
- Do not add extra features while making one test pass.
