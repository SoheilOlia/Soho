# Soho Capability Matrix

| Capability | Status | Notes |
|---|---|---|
| Goose `/soho` entrypoint | Runtime-backed | Installed by `install.sh` into Goose recipes |
| Codex plugin metadata | Runtime-backed | Present in `.codex-plugin/plugin.json` |
| Claude plugin metadata | Runtime-backed | Present in `.claude-plugin/plugin.json` |
| Cursor plugin metadata | Runtime-backed | Present in `.cursor-plugin/plugin.json` |
| Methodology skills | Prompt-backed | Real files in `skills/`, enforced by host behavior and agent discipline |
| Role catalog | Prompt-backed | Real YAML definitions in `roles/`, used to structure orchestration |
| Swarm topology choice | Prompt-backed | Real skill guidance and role contracts |
| Actual parallel agent spawning | Host-dependent | Only runtime-backed if the host exposes agent delegation tools |
| Serial role-pass fallback | Prompt-backed | Required when host cannot truly spawn agents |
| Receipt validation | Runtime-backed | Enforced by `schemas/soho-receipt.schema.json` and `scripts/validate.py` |

## Rule

If a capability is not runtime-backed in the current host, Soho must say so explicitly in the receipt.
