# Changelog

All notable changes to the homelab-hub workspace. Upstream template changes are in [TEMPLATE_CHANGELOG.md](TEMPLATE_CHANGELOG.md).

## [docs-sync] - 2026-10-18

### Changed
- docs/inventory.md: node, VM and LXC tables refreshed from the live cluster
- README.md: The live cluster has 14 LXCs.
- docs/rebuild.md: The live cluster has 14 LXCs.

## [1.0.0] - 2026-10-06

### Added
- Workspace created from [raffertyuy/repo-of-repos](https://github.com/raffertyuy/repo-of-repos) v0.6.1.
- `repos/repos.yaml` with six repos: homelab-infrastructure, homelab-deployment, helios-api, glance-dashboard, homelab-agent, blog.
- `AGENTS.md`: Morpheus persona, homelab context, repo map, source-of-truth order, safety rules, live access notes.
- Docs: `docs/architecture.md`, `docs/inventory.md` (live snapshot 2026-10-06), `docs/rebuild.md`.
- Rules: `secrets`, `iac`, `python`, `blog`.
- Skills: `/secret-scan`, `/inventory-refresh`.
- Scripts: `scripts/pull_all.py`, `scripts/secret_scan.py`.
- Draft plan: `_plans/20261006-consolidate-infra-repos.plan.md`.

### Removed
- Template `frontend.md` rule (no frontend code in this workspace).
