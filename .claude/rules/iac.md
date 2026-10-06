---
paths: ["**/*.tf", "**/*.tfvars.example", "**/*.pkr.hcl", "**/ansible/**/*.yml", "**/ansible/**/*.yaml", "**/docker-compose*.yml", "**/compose*.yml"]
---

# Infrastructure as Code

- **Plan before apply.** Show `terraform plan` / `ansible-playbook --check --diff` output before any real run.
- **Never run against live hosts** unless the owner asked for it in this session.
- Terraform `terraform/proxmox/main.tf` still defines retired K8s and syslog VMs. Don't apply it as-is.
- LXCs are not managed by Terraform. Don't add them without a plan in `_plans/`.
- Ansible runs from `ansible-controller01` (192.168.20.30). Keep playbooks idempotent.
- Pin container image tags (for example `jellyseerr:2.7.3`), not `latest`, for anything stateful.
- Compose: secrets via `env_file: .env` or `${VAR}`. Bind data to NFS paths already used by that host.
- Don't edit archived content (`Azure-Hybrid-Lab/`, `terraform/azure/`, `ansible/roles/k8s/`, `ansible/roles/opnsense/`) except to add an Archived banner.
