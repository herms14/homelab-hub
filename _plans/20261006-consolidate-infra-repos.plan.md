---
status: draft
repos: [homelab-infrastructure, homelab-deployment]
created: 2026-10-06
---

# Plan: Consolidate the Two Infra Repos

## Context

`homelab-infrastructure` and `homelab-deployment` started as one repo (shared root commit `ac0df66`, 2025-12-14) and drifted apart.

| Metric (2026-10-06) | Count |
|---------------------|-------|
| Tracked files in deployment | 503 |
| Tracked files in infrastructure | 447 |
| Identical in both | 317 |
| Same path, different content | 114 |
| Only in deployment | 72 (mostly `terraform/azure/`, `ansible/playbooks/`) |
| Only in infrastructure | 16 (Packer vars, `docs/README.md`, `CLAUDE_DESKTOP_PROJECT_DESCRIPTION.md`) |

Two copies means double edits and silent drift. Goal: one repo owns IaC + docs, the other becomes a thin rebuild guide (or is archived).

This is a **draft for the owner to decide**. Nothing here runs without approval.

## Options

| Option | Result | Effort |
|--------|--------|--------|
| A. Merge into `homelab-infrastructure`, archive `Homelab-Infrastructure-Deployment` | One repo, rebuild order lives in its README | Medium |
| B. Keep both. `homelab-deployment` keeps only README + rebuild docs and links to infra for code | Clear split, no duplicate code | Medium |
| C. Leave as is, document which is canonical (done in hub `AGENTS.md`) | No work, drift continues | None |

## Steps (Option A)

- [ ] Step 1: Audit before moving anything
  - **Task**: Run `/secret-scan --tracked` on both repos. Owner handles findings privately (rotate, then decide on history rewrite).
- [ ] Step 2: Diff the 114 changed files
  - **Task**: Use the explorer agent to classify each as "deployment newer", "infra newer" or "conflict". Use `git log -1 --format=%ad -- <file>` in each repo.
- [ ] Step 3: Bring the newer copies into `homelab-infrastructure`
  - **Files**: `repos/homelab-infrastructure/ansible/playbooks/`, `docs/`, `dashboards/`
  - **Task**: Worker scoped to infra. Copy the 72 deployment-only files that are still current (skip archived Azure Terraform unless the owner wants it kept).
- [ ] Step 4: Move the rebuild guide
  - **Files**: `repos/homelab-infrastructure/docs/REBUILD.md` (new), README link
  - **Task**: Port "Rebuild Order", "Retired / Archived" and the Terraform warning from deployment README.
- [ ] Step 5: Archive the deployment repo
  - **Files**: `repos/homelab-deployment/README.md`
  - **Task**: Replace README with a pointer to `homelab-infrastructure`. Owner archives the repo on GitHub.
- [ ] Step 6: Update the hub
  - **Files**: `repos/repos.yaml`, `repos/repos.md`, `AGENTS.md`, `docs/architecture.md`, `docs/rebuild.md`
  - **Task**: `/remove-repository homelab-deployment` (or keep it read-only), fix all links.
