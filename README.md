# 🌊 SOHO — Swarm Orchestration with Disciplined Methodology

A unified AI development recipe for [Goose](https://github.com/block/goose) that combines two paradigms:

- **[superpowers](https://github.com/obra/superpowers)** → 14 composable skills that auto-activate (brainstorming, TDD, systematic debugging, subagent-driven development, code review, verification). Process discipline for one elite agent.
- **[ruflo](https://github.com/ruvnet/ruflo)** → Multi-agent swarm orchestration with 16 specialized roles, 4 topologies, SPARC methodology, and anti-drift coordination. Team coordination for many agents.

**The result**: every agent in the swarm operates with superpowers-level discipline, and the orchestrator coordinates them with ruflo-level sophistication.

## Install

```bash
git clone https://github.com/SoheilOlia/Soho.git
cd Soho
./install.sh
```

Or manually:

```bash
cp soho.yaml ~/.config/goose/recipes/soho.yaml
```

## Use

Start a new Goose session and type:

```
/soho
```

Then describe what you want to build. SOHO handles the rest.

## Three-Mode Decision System

SOHO automatically decides whether to work solo or deploy a swarm:

| Mode | When | Receipt |
|------|------|---------|
| 🎯 **Auto-Solo** | Obvious simple tasks (typo, single edit, config tweak) | "🎯 Running solo — full discipline" |
| 🌊 **Auto-Swarm** | Obvious complex tasks (new project, 5+ files, audit, migration) | "🌊 Running as team: [agents] — [topology]" |
| 🤔 **Recommend** | Ambiguous (medium feature, unclear scope) | "🤔 This could go either way. My recommendation: ..." |

Override anytime: "swarm this" / "just do it" / "what do you think?"

## What's Inside

### 14 Auto-Activating Skills (from superpowers)

| # | Skill | Iron Law |
|---|-------|----------|
| 1 | Brainstorming | No code without design approval |
| 2 | Writing Plans | No placeholders — EVER |
| 3 | TDD | No production code without failing test first |
| 4 | Systematic Debugging | No fixes without root cause |
| 5 | Subagent-Driven Dev | Two-stage review (spec + quality) |
| 6 | Executing Plans | Follow steps exactly |
| 7 | Git Worktrees | Verify .gitignore before creating |
| 8 | Finishing a Branch | Tests must pass to proceed |
| 9 | Parallel Agents | Independent domains only |
| 10 | Requesting Code Review | Mandatory after major changes |
| 11 | Receiving Code Review | Verify before implementing |
| 12 | Verification | No claims without fresh evidence |
| 13 | Writing Skills | Gate functions, red flags, checklists |
| 14 | Root Cause Tracing | Fix at source, not symptom |

### 16 Specialized Agent Roles (from ruflo)

| Role | Specialization |
|------|----------------|
| 🎯 Coordinator | Decomposes tasks, assigns work, enforces anti-drift |
| 💻 Coder | Production code, features, TDD |
| 🧪 Tester | Tests (unit/integration/e2e), >90% coverage |
| 🔍 Reviewer | Code quality, correctness, security |
| 🏗️ Architect | System design, ADRs, interfaces |
| 🔬 Researcher | Requirements analysis, investigation |
| 🛡️ Security Architect | OWASP Top 10, CWE, secrets scanning |
| ⚡ Performance Engineer | Profiling, optimization, benchmarks |
| 📝 Documenter | Docs, API specs, guides |
| 🔧 DevOps Engineer | CI/CD, Docker, infrastructure |
| 📊 Data Engineer | Schemas, migrations, queries |
| 🎨 Frontend Specialist | UI, accessibility, responsive design |
| 📱 Mobile Specialist | iOS/Android development |
| 🧠 ML/AI Specialist | ML pipelines, model training |
| 🔄 Migration Specialist | Framework upgrades, compatibility |
| 🚀 Release Manager | Versioning, changelogs, deployment |

### 4 Swarm Topologies

- **Hierarchical** — Coordinator at top, best for coding tasks (anti-drift)
- **Mesh** — Peer-to-peer, best for research and exploration
- **Ring** — Sequential pipeline, best for CI/CD and data processing
- **Star** — Hub-and-spoke, best for parallel independent work

### 10 Sub-Recipes

Deep-dive workflows for: security audit, performance optimization, code review, architecture design, test suite generation, documentation, migration, project setup, SPARC workflow, release management.

### SPARC Methodology

**S**pecification → **P**seudocode → **A**rchitecture → **R**efinement → **C**ompletion

## Philosophy

> The marginal cost of completeness is near zero with AI. Do the whole thing. Do it right. Do it with tests. Do it with documentation. Do it so well that you are genuinely impressed — not politely satisfied, actually impressed.
>
> The standard isn't "good enough" — it's "holy shit, that's done."

## File Structure

```
Soho/
├── soho.yaml          # Main recipe (763 lines)
├── sub-recipes/       # 10 deep-dive workflows
│   ├── security-audit.yaml
│   ├── performance-optimization.yaml
│   ├── code-review.yaml
│   ├── architecture-design.yaml
│   ├── test-suite.yaml
│   ├── documentation.yaml
│   ├── migration.yaml
│   ├── project-setup.yaml
│   ├── sparc-workflow.yaml
│   └── release-management.yaml
├── install.sh         # One-command installer
├── LICENSE            # MIT
└── README.md          # This file
```

## Credits

- **superpowers** by [Jesse Vincent (obra)](https://github.com/obra/superpowers) — the skill discipline system
- **ruflo** by [Ruv (ruvnet)](https://github.com/ruvnet/ruflo) — the swarm orchestration system
- **Goose** by [Block](https://github.com/block/goose) — the platform

## License

MIT
