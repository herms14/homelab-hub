#!/usr/bin/env python3
"""Scan git changes in the hub and every repo under repos/ for likely secrets.

Usage:
  python scripts/secret_scan.py            # staged changes (git diff --cached)
  python scripts/secret_scan.py --all      # staged + unstaged + untracked
  python scripts/secret_scan.py --tracked  # every tracked file (full audit)
  python scripts/secret_scan.py --repo helios-api

Exit code 1 if anything is found. Matches are masked in the output.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("gitlab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("slack/discord token", re.compile(r"\bxox[abp]-[A-Za-z0-9-]{10,}|\b[MN][A-Za-z0-9]{23,25}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}\b")),
    ("aws key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("proxmox token", re.compile(r"PVEAPIToken=[^\s'\"]+=[0-9a-fA-F-]{36}")),
    ("uuid secret", re.compile(r"(?i)(token|secret|api[_-]?key)[\"']?\s*[:=]\s*[\"']?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")),
    ("hex api key", re.compile(r"(?i)(api[_-]?key|apikey|x-api-key|token|secret)[\"']?\s*[:=]\s*[\"']?[0-9a-f]{32,}\b")),
    ("password assignment", re.compile(r"(?i)\b(password|passwd|pwd|secret)[\"']?\s*[:=]\s*[\"']?(?!\$\{|\{\{|<|change-?me|your|example|xxx|\*{3}|os\.environ|env\(|var\.|none\b|null\b|\"\"|''|true\b|false\b)[^\s\"',;]{6,}")),
    ("url credentials", re.compile(r"[a-z]+://[^/\s:@]+:(?!\$\{)[^/\s@]{4,}@")),
]
SKIP_FILES = re.compile(r"(\.example$|\.sample$|\.lock$|package-lock\.json$|secret_scan\.py$|\.(png|jpg|jpeg|gif|ico|svg|pdf|woff2?)$)")
# Values that are code references, not literals: cfg.password, settings.x.y, PIHOLE_PASSWORD
CODE_REF = re.compile(r"[:=]\s*(?:[A-Za-z_]\w*(?:\.\w+)+|[A-Z_][A-Z0-9_]{3,})\s*[,)}\]]?\s*$")


def is_false_positive(label, matched):
    return label == "password assignment" and bool(CODE_REF.search(matched))


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout


def mask(s):
    s = s.strip()
    return s[:6] + "..." + s[-2:] if len(s) > 10 else "***"


def file_lines(repo, f):
    try:
        for i, line in enumerate((repo / f).read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            yield f, i, line
    except OSError:
        return


def lines_to_scan(repo, mode):
    """Yield (file, line_no, text)."""
    if mode == "tracked":
        for f in git(repo, "ls-files").splitlines():
            if not SKIP_FILES.search(f):
                yield from file_lines(repo, f)
        return
    diffs = [git(repo, "diff", "--cached", "-U0", "--no-color")]
    if mode == "all":
        diffs.append(git(repo, "diff", "-U0", "--no-color"))
        for f in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
            if not SKIP_FILES.search(f):
                yield from file_lines(repo, f)
    for diff in diffs:
        cur, n = None, 0
        for line in diff.splitlines():
            if line.startswith("+++ "):
                cur = line[6:] if line.startswith("+++ b/") else None
            elif line.startswith("@@"):
                m = re.search(r"\+(\d+)", line)
                n = int(m.group(1)) if m else 0
            elif line.startswith("+") and cur and not SKIP_FILES.search(cur):
                yield cur, n, line[1:]
                n += 1


def repos(only):
    found = [("homelab-hub", ROOT)]
    repo_dir = ROOT / "repos"
    if repo_dir.exists():
        for d in sorted(repo_dir.iterdir()):
            if (d / ".git").exists():
                found.append((d.name, d))
    return [r for r in found if not only or r[0] == only]


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--all", action="store_true")
    g.add_argument("--tracked", action="store_true")
    ap.add_argument("--repo")
    a = ap.parse_args()
    mode = "tracked" if a.tracked else "all" if a.all else "staged"

    hits = 0
    for name, path in repos(a.repo):
        for f, n, text in lines_to_scan(path, mode):
            for label, rx in PATTERNS:
                m = rx.search(text)
                if m and not is_false_positive(label, m.group(0)):
                    hits += 1
                    print(f"[{name}] {f}:{n}  {label}: {mask(m.group(0))}")
                    break
    print(f"\n{hits} possible secret(s) found ({mode} mode)." if hits else f"No secrets found ({mode} mode).")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
