---
paths: ["repos/blog/**"]
---

# Blog (Clustered Thoughts)

- Posts in `_posts/` are generated from the owner's Obsidian vault by `scripts/sync_obsidian.py`. Edit the vault note, not the generated post, unless the owner says otherwise.
- Only vault notes with `publish: true` are synced.
- Front matter: `title`, `date`, `categories`, `summary`. Keep the Minimal Mistakes theme conventions in `_config.yml`.
- Style: plain, first-person, no em dashes. Mark retired tech (Kubernetes, Azure hybrid lab) as past tense.
- Pushing to `main` deploys via `.github/workflows/pages-deploy.yml`. Check the Actions run after pushing.
