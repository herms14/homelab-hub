---
paths: ["repos/helios-api/**/*.py", "repos/glance-dashboard/apis/**/*.py"]
---

# Python Services

- Helios: FastAPI + Pydantic v2 + Typer CLI. Add new platforms as a provider in `api/`, a router, and CLI commands. Update `COMMANDS.md` and the README API table.
- Helios access tiers are enforced by the Proxmox token behind each instance (`:8000` full, `:8001` observer, `:8002` operator), not by app code. Don't add per-endpoint tier checks without a plan.
- Glance helper APIs: small Flask apps returning JSON for Glance `custom-api` widgets. One folder per API under `apis/`, each with its own compose file.
- Config from environment variables. No hardcoded hosts, keys or personal data (for example birth dates). Use safe defaults.
- Keep files UTF-8. Validate with `python -m py_compile` at minimum.
