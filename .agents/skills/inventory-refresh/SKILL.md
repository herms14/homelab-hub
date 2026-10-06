---
name: inventory-refresh
description: Compare the live Proxmox cluster against docs/inventory.md, report drift, and update the hub and repo docs on approval
user-invocable: true
---

# Inventory Refresh

Check the live MorpheusCluster against [docs/inventory.md](../../../docs/inventory.md) and fix drift.

Needs a machine on the homelab network with SSH access to a Proxmox node. If SSH fails, stop and say so. Never guess values.

## Steps

1. **Collect (read-only)**:
   ```bash
   ssh node01 "pveversion; pvecm status | grep -E 'Quorate|Nodes'"
   ssh node01 "pvesh get /cluster/resources --type vm --output-format json"
   ssh node01 "pvesh get /cluster/resources --type node --output-format json"
   ```
   For a guest's IP: `pct config <ctid> | grep net0` (LXC) or the guest agent (VM).
   If the workstation can't reach a host, hop through `codex-agent-lxc` (192.168.40.16).
2. **Diff** against `docs/inventory.md`: version, nodes (CPU/RAM), VMs, LXCs (ID, name, node, RAM, status, IP).
3. **Report** a drift table:

   | Item | Docs | Live | Action |
   |------|------|------|--------|

4. **Ask** the owner before changing anything.
5. **Update on approval**, one repo at a time (writes are single-repo):
   - `docs/inventory.md` here (bump the snapshot date)
   - `repos/homelab-infrastructure/README.md` (Inventory + Infrastructure at a Glance) and its `CHANGELOG.md`
   - `repos/homelab-deployment/README.md` and `docs/INVENTORY.md`, plus its `CHANGELOG.md`
6. Run `/secret-scan`, then `/commit-all-repos`.

## Rules

- Read-only on the cluster. Never start, stop or change guests here.
- Don't add credentials, tokens or private notes to any doc.
- A stopped guest stays in the inventory, marked **stopped**. Only remove guests that no longer exist.
