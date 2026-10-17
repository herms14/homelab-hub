# Rebuild Order

How to rebuild the whole homelab from bare metal, across all repos.
Detailed per-step instructions live in [`repos/homelab-deployment/README.md`](../repos/homelab-deployment/README.md#rebuild-order-from-bare-metal). This page adds the cross-repo view.

> [!TIP]
> If PBS and the Synology NAS survived, restore guests from backup at step 4. That's faster than steps 5-11.

## Prerequisites

- Hardware: 3 Proxmox nodes, QDevice host, Synology DS920+, Omada gateway/switches/APs
- Run `/pull-all-repos` in this hub so all six repos are present
- Secrets from your password manager (never from a repo): Proxmox API tokens, Cloudflare DNS token, Authentik, Arr keys, Discord/GitLab tokens

## Steps

| # | Step | Repo | Start here |
|---|------|------|-----------|
| 1 | Network and VLANs (Omada) | `homelab-deployment` | `docs/NETWORKING.md` |
| 2 | Proxmox cluster + QDevice | `homelab-deployment` | `docs/PROXMOX.md` |
| 3 | Storage (Synology NFS) | `homelab-deployment` | `docs/STORAGE.md` |
| 4 | PBS: restore or fresh install | `homelab-deployment` | `docs/PBS_DEPLOYMENT.md`, `docs/PBS_DISASTER_RECOVERY.md` |
| 5 | Templates (Ubuntu cloud-init, Packer Windows) | `homelab-deployment` | `packer/`, `docs/PACKER.md` |
| 6 | VMs via Terraform | `homelab-deployment` | `terraform/proxmox/` (prune retired K8s/syslog VMs first) |
| 7 | Ansible bootstrap + Docker | `homelab-deployment` | `docs/ANSIBLE.md`, `ansible/roles/docker/` |
| 8 | Core: Pi-hole, Traefik, Authentik | `homelab-deployment` | `ansible/roles/traefik/`, `ansible/roles/authentik/`, `docs/FORWARD_AUTH_SETUP.md` |
| 9 | Apps: media, Immich, GitLab, Paperless, n8n, Home Assistant, etc. | `homelab-deployment` | `ansible/playbooks/`, `docs/SERVICES.md` |
| 10 | Monitoring: Prometheus, Grafana, Uptime Kuma, exporters | `homelab-infrastructure` | `ansible/playbooks/monitoring/`, `dashboards/` |
| 11 | Glance + widget APIs | `glance-dashboard` | `README.md#deploy`, `config/.env.example`, `apis/` |
| 12 | Helios API (CT210) | `helios-api` | `README.md#deployment` (Option A), `deploy/systemd/` |
| 13 | Codex patch agent (CT211) | not published | `homelab-deployment` README, "Autonomous Patch Management Pipeline" |
| 14 | Docs and story | `homelab-infrastructure`, `blog` | Update inventory, then `/inventory-refresh` here |

## Notes

- **LXCs are not in Terraform.** All 14 were created by hand. Restore from PBS or recreate with `pct create`, then run the matching playbook.
- **Packer:** both infra repos have the same Windows templates (2022, 2025, Windows 11). Build vars come from a local `*.pkrvars.hcl` that you never commit.
- **Glance:** use `glance-dashboard`, not the older Glance playbooks in the infra repos.
- **Secrets:** every repo uses `.env.example` / `*.tfvars.example`. Fill real values on the host only.

## Verify After Rebuild

| Check | Command / URL |
|-------|---------------|
| Cluster quorate | `pvecm status` |
| Guests up | `pvesh get /cluster/resources --type vm` |
| DNS | `nslookup glance.hrmsmrflrii.xyz 192.168.90.53` |
| Edge + SSO | `https://auth.hrmsmrflrii.xyz`, `https://traefik.hrmsmrflrii.xyz` |
| Dashboards | `https://glance.hrmsmrflrii.xyz`, `https://grafana.hrmsmrflrii.xyz` |
| Helios | `curl http://192.168.40.14:8000/health` |
| Backups | PBS UI `https://192.168.20.50:8007`, check last job |
