# Soho Capability Matrix

| Capability | Status | Notes |
|---|---|---|
| Goose recipe entrypoint | Runtime-backed | Installed by `install.sh` into Goose recipes and opened with `goose recipe open soho`; it is not a slash command inside an existing chat |
| Codex skills install | Runtime-backed | Installed as `~/.agents/skills/soho`; public marketplace visibility is not claimed |
| Claude local marketplace metadata | Runtime-backed | Present in `.claude-plugin/plugin.json`; host still requires `claude plugin marketplace add` and `claude plugin install` |
| Cursor local plugin metadata | Host-dependent | Present in `.cursor-plugin/plugin.json`; discovery depends on Cursor's local plugin support/version |
| Methodology skills | Prompt-backed | Real files in `skills/`, enforced by host behavior and agent discipline |
| Role catalog | Prompt-backed | Real YAML definitions in `roles/`, used to structure orchestration |
| Swarm topology choice | Prompt-backed | Real skill guidance and role contracts |
| Actual parallel agent spawning | Host-dependent | Only runtime-backed if the host exposes agent delegation tools |
| Serial role-pass fallback | Prompt-backed | Required when host cannot truly spawn agents |
| Receipt validation | Runtime-backed | Enforced by `schemas/soho-receipt.schema.json` and `scripts/validate.py` |

## Rule

If a capability is not runtime-backed in the current host, Soho must say so explicitly in the receipt.
