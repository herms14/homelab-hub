# homelab-hub

> **Based on [raffertyuy/repo-of-repos](https://github.com/raffertyuy/repo-of-repos).** This is a homelab-specific implementation of that template. Run `/sync-template` now and then to pick up improvements.

One workspace for everything about my homelab, **MorpheusCluster**. It pulls all six homelab repos into `repos/` so an AI agent (or I) can see and change them together. Each repo still keeps its own git history and pushes to its own GitHub remote.

**Meet Morpheus**, the agent that runs this workspace. It reads across every repo, checks claims against the live cluster, and delegates single-repo changes to scoped workers.

> **The pattern in one sentence:** an outer "agent" repo pulls in all related repos under `repos/`, while commits still flow back to each repo's own origin. Write-up: **[Repo-of-Repos pattern](https://raffertyuy.com/raztype/repo-of-repos-pattern/)**.

## The Repos

| Folder | GitHub | What it is |
|--------|--------|-----------|
| [`homelab-infrastructure`](https://github.com/herms14/homelab-infrastructure) | herms14/homelab-infrastructure | Main docs: current state, service catalog, Ansible / Terraform / Packer |
| [`homelab-deployment`](https://github.com/herms14/Homelab-Infrastructure-Deployment) | herms14/Homelab-Infrastructure-Deployment | Bare-metal rebuild guide |
| [`helios-api`](https://github.com/herms14/helios-homelab-api) | herms14/helios-homelab-api | Helios: control-plane REST API + CLI for Proxmox, Synology, Omada |
| [`glance-dashboard`](https://github.com/herms14/glance-dashboard) | herms14/glance-dashboard | Glance dashboard config + custom widget APIs |
| [`homelab-agent`](https://github.com/herms14/homelab-agent) | herms14/homelab-agent | Reusable AI slash commands for homelab docs |
| [`blog`](https://github.com/herms14/Clustered-Thoughts) | herms14/Clustered-Thoughts | [Clustered Thoughts](https://herms14.github.io/Clustered-Thoughts/), the homelab blog |

Details per repo: [repos/repos.md](repos/repos.md).

## The Lab in 30 Seconds

| | |
|---|---|
| **Hypervisor** | Proxmox VE 9.2, 3 nodes + QDevice (64 threads, ~120 GB RAM) |
| **Guests** | 5 VMs + 3 templates, 13 LXCs |
| **Network** | TP-Link Omada SDN, 8 VLANs |
| **Edge** | Traefik + Let's Encrypt, Authentik SSO, Pi-hole DNS |
| **Storage / backup** | Synology DS920+ (NFS), Proxmox Backup Server |
| **Automation** | Ansible, Terraform, Packer, GitLab CI, Helios, an approval-gated AI patch agent |
| **Apps** | Jellyfin + Arr stack, Immich, GitLab, Home Assistant, Paperless, n8n, Grafana, Glance, more |

## Documentation

| Doc | What's in it |
|-----|-------------|
| [docs/architecture.md](docs/architecture.md) | Lab diagram, which repo owns what, cross-repo touchpoints |
| [docs/inventory.md](docs/inventory.md) | Live snapshot: nodes, VMs, LXCs, ports, VLANs |
| [docs/rebuild.md](docs/rebuild.md) | Full rebuild order from bare metal, across all repos |
| [AGENTS.md](AGENTS.md) | Instructions for AI agents: source of truth, safety rules |
| [_plans/](_plans/) | Cross-repo plans (for example consolidating the two infra repos) |

## Getting Started

```bash
git clone https://github.com/herms14/homelab-hub.git
cd homelab-hub
python scripts/pull_all.py        # clones all six repos into repos/
```

Then open the folder in VS Code, Claude Code, Copilot CLI or Codex. With an agent, run `/pull-all-repos` instead; it also refreshes `repos/repos.md`.

Before committing anywhere:

```bash
python scripts/secret_scan.py     # staged changes in the hub and every repo
```

## Working in the Hub

- **Ask across repos**: "Where is the nas-backup-status API defined, and which repo is current?"
- **Plan first** for multi-repo changes: `/create-plan Move Glance helper APIs out of the infra repos`, review the plan in `_plans/`, then `/implement-plan`.
- **Check drift**: `/inventory-refresh` compares the live cluster to [docs/inventory.md](docs/inventory.md).
- **Ship**: `/secret-scan`, then `/commit-all-repos`. Each repo gets its own commit and push.

See [_plans/README.md](_plans/README.md) for the plan format.

## Project Structure

```
.
├── AGENTS.md                          # Canonical instructions for ALL AI agents
├── CLAUDE.md                          # One-line pointer: @AGENTS.md
├── TEMPLATE_VERSION                   # Upstream template version
├── TEMPLATE_CHANGELOG.md              # Upstream template changelog
├── .mcp.json                          # MCP servers (Claude Code, Copilot, VS Code 1.118+)
├── .agents/skills/                    # Canonical skills (incl. secret-scan, inventory-refresh)
├── .claude/
│   ├── agents/                        # explorer, worker, reviewer
│   ├── rules/                         # secrets, iac, python, blog
│   ├── skills/                        # Skill stubs → .agents/skills/
│   └── prompt-snippets/               # Shared instructions
├── .codex/config.toml                 # Codex MCP mirror
├── .vscode/settings.json              # Search excludes, git scan depth
├── _plans/                            # Cross-repo implementation plans
├── docs/
│   ├── architecture.md                # Lab + repo map
│   ├── inventory.md                   # Live snapshot
│   ├── rebuild.md                     # Cross-repo rebuild order
│   └── adding-repos.md, workspace-manifest.md, cross-tool-sync.md  (template docs)
├── scripts/
│   ├── pull_all.py                    # Clone/pull every repo (no agent needed)
│   └── secret_scan.py                 # Pre-commit secret scan across all repos
└── repos/
    ├── repos.yaml                     # Workspace manifest
    ├── repos.md                       # Repo descriptions
    ├── homelab-infrastructure/        # git origin = herms14/homelab-infrastructure
    ├── homelab-deployment/            # git origin = herms14/Homelab-Infrastructure-Deployment
    ├── helios-api/                    # git origin = herms14/helios-homelab-api
    ├── glance-dashboard/              # git origin = herms14/glance-dashboard
    ├── homelab-agent/                 # git origin = herms14/homelab-agent
    └── blog/                          # git origin = herms14/Clustered-Thoughts
```

Everything under `repos/<name>/` is gitignored here. This repo only tracks the workspace: instructions, skills, plans and docs.

## Slash Commands

Invoked with `/<name>` in Claude Code, GitHub Copilot, or OpenAI Codex. Canonical definitions live in `.agents/skills/` (Copilot and Codex read them natively); `.claude/skills/` holds thin stubs for Claude Code.

### Workspace

| Command | What it does |
|---------|-------------|
| `/pull-all-repos` | Clone/pull all repos, verify local folders, regenerate `repos.md` |
| `/add-repository <url>` | Clone a git repo and register it |
| `/add-repository --local <name>` | Create/register a local source folder |
| `/remove-repository <name>` | Remove a repo/folder from config |
| `/clean-repos` | Remove stale entries whose directories no longer exist |

### Plan & Implement

| Command | What it does |
|---------|-------------|
| `/create-plan <description>` | Create an implementation plan with steps, context, and pseudocode |
| `/implement-plan [plan-file]` | Execute a plan — build, test, fix, and update the plan as you go |

### Git

| Command | What it does |
|---------|-------------|
| `/commit` | Stage, commit, and push root workspace only (excludes `repos/`) |
| `/commit-all-repos` | Stage, commit, and push each sub-repo, then root workspace |
| `/pr-all-repos` | Create PRs in all sub-repos, cross-link as siblings |

### Docs & Maintenance

| Command | What it does |
|---------|-------------|
| `/update-all-md-docs` | Sync all markdown files with current state |
| `/sync-template` | Pull latest template updates from upstream |

### Homelab

| Command | What it does |
|---------|-------------|
| `/secret-scan` | Scan staged (or all) changes in every repo for secrets before committing |
| `/inventory-refresh` | Compare the live Proxmox cluster with `docs/inventory.md`, fix drift on approval |

The [homelab-agent](https://github.com/herms14/homelab-agent) commands (`/lab-status`, `/runbook`, `/doc-sync`, ...) live in `repos/homelab-agent/commands/`. Copy them into `.claude/commands/` if you want them here too.

## Agents

The workspace uses three specialized agents. Defined once in `.claude/agents/` — read natively by both Claude Code and GitHub Copilot (VS Code and CLI). Codex doesn't support custom agents yet.

| Agent | Scope | Purpose |
|-------|-------|---------|
| **explorer** | Read-only, all repos | Trace dependencies, find types, answer "what breaks if I change X?" Has `Bash` for git/search; read-only by instruction. |
| **worker** | Write-scoped, one repo | Implement changes. Follows the target repo's own instructions. |
| **reviewer** | Read-only | Code review against shared standards. |

**Key rule: reads are cross-repo, writes are single-repo.** The explorer reads across all repos. The worker only writes to one repo at a time. The orchestrator (Morpheus) coordinates by spawning scoped workers. This prevents wrong-directory mistakes and accidental cross-repo edits.

## MCP Servers

Configured in `.mcp.json` (Claude Code, Copilot, VS Code 1.118+) and mirrored in `.codex/config.toml` (Codex):

| Server | Purpose |
|--------|---------|
| [Context7](https://github.com/upstash/context7) | Library/framework docs |
| [Playwright](https://github.com/microsoft/playwright-mcp) | Browser automation |

## Keeping Up to Date

This template evolves. To pull the latest changes:

```
/sync-template
```

This checks your `TEMPLATE_VERSION`, copies updated framework files, and smart-merges files that mix template and project content. It never touches your repos, plans, settings, or MCP config.

See `TEMPLATE_CHANGELOG.md` for what's new in each version.

## Further Reading

| Topic | Where |
|-------|-------|
| Adding repos and local folders | [docs/adding-repos.md](docs/adding-repos.md) |
| Workspace manifest format | [docs/workspace-manifest.md](docs/workspace-manifest.md) |
| Cross-tool sync (Claude Code + Copilot + Codex) | [docs/cross-tool-sync.md](docs/cross-tool-sync.md) |
| Plan file format | [_plans/README.md](_plans/README.md) |

## Customization

- **`AGENTS.md`** — project context, architecture, data flows (canonical for all tools)
- **Skills** — add canonical `SKILL.md` in `.agents/skills/<name>/` plus a stub in `.claude/skills/<name>/`
- **`.claude/rules/`** — auto-apply rules by file glob (this hub: secrets, iac, python, blog)
- **`.claude/prompt-snippets/`** — shared instructions used by 2+ features
- **Agents** — add or customize in `.claude/agents/` (read by Claude Code and Copilot)
- **MCP servers** — add to both `.mcp.json` and `.codex/config.toml`
- **Per-repo instructions** — repos can have their own `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`

## Prior Art & Inspiration

This template builds on ideas from the community:

| Feature | Inspired by |
|---------|-------------|
| Plan-implement workflow | [Plan-Implement-Run](https://raffertyuy.com/raztype/vibe-coding-plan-implement-run/) — structured plan/implement/run phases with living plan documents |
| Read/write separation (explorer + worker agents) | [ttal](https://dev.to/neil_agentic/how-i-manage-15-repos-with-claude-code-without-losing-my-mind-2ood) — neil_agentic's read/write split across 15+ repos |
| Workspace manifest (`repos.yaml`) | [Virtual Monorepo](https://medium.com/devops-ai/the-virtual-monorepo-pattern-how-i-gave-claude-code-full-system-context-across-35-repos-43b310c97db8) — Owen Zanzal's `.repos` clone script; [Superblocks](https://www.superblocks.com/blog/a-single-dev-workspace-for-ai-agents) `repos.yaml` manifest |
| Cross-repo PR linking (`/pr-all-repos`) | [Superblocks](https://www.superblocks.com/blog/a-single-dev-workspace-for-ai-agents) — `just pr` with sibling PR URL injection |
| Repo-scoped planning | [Spine Pattern](https://tsoporan.com/blog/spine-pattern-multi-repo-ai-development/) — Titus Soporan's prefix-based task scoping |
| Context distillation in plans | [Context from Internal Repos](https://elite-ai-assisted-coding.dev/p/context-from-internal-git-repos) — CI/CD-driven context extraction |
| Cross-tool sync (Claude + Copilot + Codex) | [Claude + Copilot + Codex Cross-Compatibility](https://raffertyuy.com/raztype/claude-copilot-codex-cross-compatibility/) — one canonical file per feature across all three tools |

Also worth reading:
- [Polyrepo Synthesis](https://rajiv.com/blog/2025/11/30/polyrepo-synthesis-synthesis-coding-across-multiple-repositories-with-claude-code-in-visual-studio-code/) — Rajiv Pant, unified VS Code workspace across repos
- [The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/) — Addy Osmani, multi-agent coordination patterns

## Template Customizations

What this hub changed from the upstream template:

- Persona: **Morpheus** (calm homelab operator) instead of Tony Stark.
- Removed `.claude/rules/frontend.md` (no frontend code here). Don't re-add it on `/sync-template`.
- Added rules: `secrets`, `iac`, `python`, `blog`.
- Added skills: `/secret-scan`, `/inventory-refresh`.
- Added `scripts/`, `docs/architecture.md`, `docs/inventory.md`, `docs/rebuild.md`.

## License

MIT. Template (c) Rafferty Uy, homelab content (c) Hermes Miraflor II. See [LICENSE](LICENSE).
