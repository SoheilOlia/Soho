---
name: using-soho
description: "Use when starting any build, debugging, review, research, planning, implementation, or multi-agent conversation that should follow Soho discipline: choose solo/swarm/recommend mode, avoid fake orchestration, verify claims, and end substantive work with a receipt."
---

# Using Soho

Use Soho when the task needs disciplined execution, explicit orchestration, or both. Load this skill before any other Soho skill, then choose the smallest mode that can honestly satisfy the request.

## Core Decision

Before doing real work, decide the mode:

| Mode | Use When | Required Output |
|---|---|---|
| `solo` | One agent can inspect, decide, implement, verify, and summarize without losing quality. | State `mode: solo`, the evidence target, and the verification command or artifact. |
| `swarm` | Independent roles or perspectives materially improve coverage, or the work has separable lanes. | State `mode: swarm`, topology, roles, write boundaries, synthesis point, and runtime. |
| `recommend` | The request is ambiguous, high-risk, or needs a direction choice before edits. | State `mode: recommend`, 2-3 options if useful, one recommendation, tradeoffs, and the trigger to proceed. |

Prefer `solo` unless `swarm` changes the quality or speed of the result. Do not use `swarm` to make ordinary work sound bigger.

## Execution Contract

If the user asks for an outcome, proceed in the selected Soho mode without waiting for a second approval. If the user asks only for a review, recommendation, plan, or prompt, stay in that output mode.

Respect explicit opt-outs:

- Skip Soho discipline: `no Soho`, `skip Soho`, `plain answer`, `no receipt`.
- Stay read-only or constrained: `read-only`, `review-only`, `dry-run`, `plan-only`, `no edits`, `no commit`, `no push`.

Confirm before high-blast-radius or externally visible actions: force-push, push to protected `main`, merge PRs, delete branches, delete files beyond a narrow task-scoped change, rewrite user-owned work, skip hooks with `--no-verify`, run `git reset --hard` or `git clean -fd`, rebase published history, run `rm -rf` outside the repo, mutate production data, kill processes you did not start, or send Slack/Linear/email messages.

## Rules

1. Do not implement creative changes until the design is clear.
2. Do not edit through a multi-step task without a written plan.
3. Do not claim orchestration that the host did not actually perform.
4. If the host cannot spawn agents, use serial role passes and record `runtime: prompt-backed`.
5. If real subagents or host-native orchestration ran, record `runtime: runtime-backed`.
6. If the runtime depends on host behavior you did not verify, record `runtime: host-dependent`.
7. End substantive work with a Soho receipt unless the user explicitly opted out.

## When to Load Other Soho Skills

- `brainstorming` for design and requirements shaping
- `writing-plans` for multi-step implementation work
- `test-driven-development` for behavior changes
- `systematic-debugging` for bugs or failing tests
- `verification-before-completion` before saying a task is done
- `orchestrating-swarms` when the task should decompose across roles
- `selecting-topology` after choosing `swarm`
- `subagent-driven-development` after a plan exists and bounded tasks are ready to execute
- `synthesizing-results` after multiple role outputs exist

## Docs Location

When a Soho child skill needs to write a spec, plan, or receipt, use `$SOHO_DOCS_DIR` if it is set. Otherwise use the current project's `docs/` tree. If there is no safe project docs directory, keep the artifact inline and say it was not written to disk.

## Receipt Contract

Every substantive Soho run should record the fields required by `schemas/soho-receipt.schema.json`:

- generated_at
- host
- mode
- runtime
- task summary
- evidence
- outputs
- confidence

Include `topology` and `roles` for swarm work.

Minimal receipt shape:

```json
{
  "generated_at": "2026-04-29T00:00:00Z",
  "host": "codex",
  "mode": "solo",
  "runtime": "prompt-backed",
  "task_summary": "Tightened Soho skill instructions and verified mirror parity.",
  "evidence": ["python3 scripts/validate.py", "python3 -m unittest discover -s tests -p 'test_*.py'"],
  "outputs": ["Updated skills/using-soho/SKILL.md"],
  "confidence": "high"
}
```

## Completion Check

Before final response, verify:

- the chosen mode and runtime are stated honestly
- claimed files, tests, PRs, installs, or external actions actually happened
- generated artifacts or receipts do not overclaim host capabilities
- unresolved risks have an owner or next action
