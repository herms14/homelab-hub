# Inventory

Snapshot of the live cluster, taken **2026-10-23** from node01 (`pvesh get /cluster/resources`).
Run `/inventory-refresh` to check for drift.

## Cluster

| Item | Value |
|------|-------|
| Name | MorpheusCluster (3 nodes + QDevice, quorate) |
| Proxmox VE | pve-manager 9.2.21, kernel 7.0.14-20-pve |
| Storage | Synology DS920+ NFS at 192.168.20.32 (`VMDisks`, `ISOs`, app data, media) |
| Backup | Proxmox Backup Server, CT100, 192.168.20.50:8007 |

| Node | Mgmt IP | CPU | RAM |
|------|---------|-----|-----|
| node01 | 192.168.20.20 | 16 | 61 GB |
| node02 | 192.168.20.21 | 16 | 28 GB |
| node03 | 192.168.20.22 | 32 | 31 GB |

Bare metal outside the cluster: **homelab-dns01** (mini PC, Ubuntu 26.04, 4 cores, 4 GB), 192.168.90.60 static, Technitium DNS `:53` / web `:5380` (https://dns.hrmsmrflrii.xyz), exporters `:9274` (Technitium) and `:9100`.

## Virtual Machines (5 running + 3 templates)

| VMID | Name | Node | RAM | IP | Role |
|------|------|------|-----|----|------|
| 103 | ansible-controller01 | node01 | 8 GB | 192.168.20.30 | Ansible / Terraform / Packer controller |
| 106 | gitlab-vm01 | node03 | 12 GB | 192.168.40.23 | GitLab CE |
| 107 | docker-vm-core-utilities01 | node01 | 32 GB | 192.168.40.13 | Monitoring, productivity apps, Glance helper APIs |
| 108 | immich-vm01 | node03 | 24 GB | 192.168.40.22 | Immich photos |
| 121 | gitlab-runner-vm01 | node02 | 2 GB | 192.168.40.24 | GitLab CI runner |
| 1000 | tpl-ubuntuv24.04-v1 | node01 | - | - | Ubuntu 24.04 template |
| 9022 | WS2022-Template | node03 | - | - | Windows Server 2022 template |
| 9025 | WS2025-Template | node03 | - | - | Windows Server 2025 template |

## LXC Containers (15, 15 running)

| CTID | Name | Node | RAM | IP | Role |
|------|------|------|-----|----|------|
| 100 | pbs-server | node03 | 4 GB | 192.168.20.50 | Proxmox Backup Server |
| 200 | docker-lxc-glance | node01 | 4 GB | 192.168.40.12 | Glance `:8080`, proxmox-nodes-api `:5061`, pihole-stats-api `:5055` |
| 201 | docker-lxc-bots | node01 | 2 GB | 192.168.40.17 | Bot host (re-IP'd from .14 on 2026-10-05) |
| 202 | pihole | node01 | 1 GB | 192.168.90.53 | Pi-hole + Unbound DNS (secondary; local names synced from Technitium) |
| 203 | traefik-lxc | node01 | 2 GB | 192.168.40.20 | Traefik reverse proxy |
| 204 | authentik-lxc | node02 | 4 GB | 192.168.40.21 | Authentik SSO |
| 205 | docker-lxc-media | node01 | 8 GB | 192.168.40.11 | Jellyfin + Arr stack |
| 206 | homeassistant-lxc | node01 | 4 GB | 192.168.40.25 | Home Assistant |
| 207 | chronicle-lxc | node02 | 2 GB | 192.168.40.15 | Homelab Chronicle |
| 208 | ghostfolio-lxc | node02 | 4 GB | 192.168.40.26 | Ghostfolio |
| 209 | homepage-lxc | node01 | 1 GB | 192.168.40.27 | Homepage |
| 210 | helios-lxc | node01 | 2 GB | 192.168.40.14 | Helios API `:8000` / `:8001` / `:8002` |
| 211 | codex-agent-lxc | node01 | 4 GB | 192.168.40.16 | Roundtable agents and portal (`boss`, `olympus-portal` :8088, `labfeed` :8790), Codex patch-management agent (`sre-agent.service`) |
| 212 | study-lxc | node02 | 2 GB | 192.168.40.38 | Study notebook (https://study.hrmsmrflrii.xyz) |
| 213 | openbao-lxc | node02 | 1 GB | 192.168.40.39 | OpenBao secrets store (:8200 TLS, https://bao.hrmsmrflrii.xyz LAN-only); auto-unseal from a no-backup mount |

## Services on docker-vm-core-utilities01 (192.168.40.13)

| Service | Port |
|---------|------|
| Uptime Kuma (DNS checks for both DNS servers; scraped by Prometheus) | 3001 |
| Prometheus | 9090 |
| Grafana | 3030 |
| n8n | 5678 |
| Paperless-ngx | 8000 |
| Karakeep | 3005 |
| Speedtest Tracker | 3000 |
| life-progress API | 5051 |
| steam-stats API | 5055 |
| gaming-pc-stats API | 5056 |
| power-control-api | 5057 |
| service-version-api | 5070 |
| nas-backup-status-api | 9102 |

## Public Endpoints

All web UIs: `https://<service>.hrmsmrflrii.xyz` through Traefik + Authentik.
Full service catalog: [`repos/homelab-infrastructure/README.md`](../repos/homelab-infrastructure/README.md#service-catalog).

## Network

| VLAN | Network | Purpose |
|------|---------|---------|
| 1 | 192.168.0.0/24 | Gateway / controller |
| 10 | 192.168.10.0/24 | Workstations |
| 20 | 192.168.20.0/24 | Homelab: Proxmox nodes, Ansible, NAS, PBS |
| 30 | 192.168.30.0/24 | IoT |
| 40 | 192.168.40.0/24 | Production apps |
| 50 | 192.168.50.0/24 | Guest Wi-Fi |
| 60 | 192.168.60.0/24 | Sonos |
| 90 | 192.168.90.0/24 | Management, DNS (Technitium .60 primary, Pi-hole .53 secondary) |
