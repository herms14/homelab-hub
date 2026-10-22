# Changelog

All notable changes to the homelab-hub workspace. Upstream template changes are in [TEMPLATE_CHANGELOG.md](TEMPLATE_CHANGELOG.md).

## [docs-sync] - 2026-10-23

### Changed
- docs/inventory.md: node, VM and LXC tables refreshed from the live cluster

## [repos] - 2026-10-19

### Added
- `roundtable` (public, homelab-only edition of the Roundtable agents), `homelab-docs` (redacted vault notes) and `vlan-flow` in repos.yaml, repos.md, README and docs/architecture.md.

### Changed
- README: the private `olympus-agents` row replaced by `roundtable`; nine repos; note that `homelab-infrastructure` and `helios-api` are private.
- docs/architecture.md, docs/rebuild.md: Roundtable paths point to `roundtable/`.

## [docs-sync] - 2026-10-19

### Changed
- docs/inventory.md: node, VM and LXC tables refreshed from the live cluster
- docs/rebuild.md: LIVE lists 15 LXCs; the previous count of 14 is wrong. Whether they were all created by hand is not verifiable from LIVE.

## [docs-secrets] - 2026-10-18

### Changed
- README.md, AGENTS.md: OpenBao secrets store and the Varys keeper agent; 15 LXCs.
- docs/architecture.md: openbao-lxc in the lab diagram; Secrets touchpoint.
- docs/inventory.md: CT213 openbao-lxc; CT212 role described.
- docs/rebuild.md: OpenBao restore step before the Roundtable agents.

## [docs-dns] - 2026-10-18

### Changed
- README.md, AGENTS.md: Technitium on homelab-dns01 is the primary DNS, Pi-hole the secondary; `olympus-agents` row lists DNS checks, dependency map, IP map and the Technitium setup.
- docs/architecture.md: homelab-dns01 in the lab diagram, request path, DNS records touchpoint.
- docs/inventory.md: homelab-dns01 (bare metal), Pi-hole secondary, Uptime Kuma DNS checks, VLAN 90.
- docs/rebuild.md: Technitium in the core rebuild step; DNS check against both servers.

## [docs] - 2026-10-18

### Changed
- README.md: `olympus-agents` row describes the portal Overview, themes, live Hermes Lab Atlas and Lab Feed.
- docs/architecture.md: Roundtable on codex-agent-lxc (CT211) in the lab diagram and repo map; `olympus-agents` deploy row; Glance pages and Lab Feed; Lab Atlas layout touchpoint.
- docs/inventory.md: CT211 runs the Roundtable services as well as the patch agent.

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
