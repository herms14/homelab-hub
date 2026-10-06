#!/usr/bin/env python3
"""Clone or fast-forward every git repo listed in repos/repos.yaml.

For people (or CI) without an AI agent. Agents should use /pull-all-repos,
which also regenerates repos/repos.md.

Usage: python scripts/pull_all.py
No third-party packages needed.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "repos" / "repos.yaml"


def load_manifest():
    entries, cur = [], None
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        if raw.lstrip().startswith("#"):
            continue
        m = re.match(r"\s*-\s*name:\s*(\S+)", raw)
        if m:
            cur = {"name": m.group(1), "type": "git", "branch": "main"}
            entries.append(cur)
            continue
        m = re.match(r"\s+(url|branch|type):\s*(\S+)", raw)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2)
    return [e for e in entries if e["type"] == "git"]


def run(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    print(f"{'repo':<26} status")
    for e in load_manifest():
        dest = ROOT / "repos" / e["name"]
        if not dest.exists():
            code, out = run("clone", "-q", "-b", e["branch"], e["url"], str(dest))
            status = "cloned" if code == 0 else f"ERROR: {out.splitlines()[-1] if out else code}"
        else:
            run("-C", str(dest), "fetch", "--all", "--prune", "-q")
            code, _ = run("-C", str(dest), "pull", "--ff-only", "-q")
            if code != 0:
                status = "SKIPPED (not fast-forward or local changes)"
            else:
                _, head = run("-C", str(dest), "log", "-1", "--format=%h %s")
                status = f"up to date: {head[:60]}"
        print(f"{e['name']:<26} {status}")


if __name__ == "__main__":
    main()
