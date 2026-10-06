---
description: Secret handling for every public repo in this workspace
---

# Secrets

Every repo here is public on GitHub.

- Never write real credentials into any file: API keys, tokens, passwords, private keys, Proxmox token secrets, Discord/GitLab tokens, Cloudflare tokens.
- Use placeholders: `${VAR_NAME}` in YAML/compose, `os.environ["VAR_NAME"]` in Python, `var.name` in Terraform.
- Ship an example file next to the real one: `.env.example`, `terraform.tfvars.example`, `*.pkrvars.hcl.example`.
- Never stage `.env`, `*.tfvars`, `*.pkrvars.hcl`, `*.pem`, `*.key`, `id_*`.
- If you find a real secret already committed: do not repeat it in output, commits, docs or plans. Tell the owner privately so they can rotate it.
- Run `/secret-scan` before any commit.
