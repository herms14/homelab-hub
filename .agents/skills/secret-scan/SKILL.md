---
name: secret-scan
description: Scan staged (or all) changes in the hub and every repo under repos/ for secrets before committing
user-invocable: true
---

# Secret Scan

Every repo in this workspace is public. Run this before any commit, including inside `/commit` and `/commit-all-repos`.

## Arguments

- `/secret-scan` — staged changes in all repos (default)
- `/secret-scan --all` — staged, unstaged and untracked changes
- `/secret-scan --tracked` — every tracked file (full audit, slow)
- `/secret-scan --repo <name>` — one repo only (`homelab-hub` for the root)

## Steps

1. Run `python scripts/secret_scan.py <args>` from the workspace root.
2. Exit code 0: report "No secrets found" and continue.
3. Exit code 1: for each hit, open the file at that line and decide:
   - **Real secret** → stop. Replace it with a placeholder (`${VAR}`, `os.environ[...]`, `var.x`), add the variable to the matching `.env.example`, unstage, re-run the scan. Tell the owner the secret may need rotating.
   - **False positive** (placeholder, docs example, hash, test fixture) → note why, and continue.
4. Never print the full secret value. The script already masks matches; keep it that way.

## Also check

- No `.env`, `*.tfvars`, `*.pkrvars.hcl`, `*.pem`, `*.key` or `id_*` files are staged (`git diff --cached --name-only`).
- Pre-existing secrets found with `--tracked` are **not** fixed by a normal commit; they stay in history. Report them to the owner privately. Do not write them into this public repo (no plans, docs or issues listing them).
