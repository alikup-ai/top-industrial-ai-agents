#!/usr/bin/env python3
"""
Update GitHub star counts for projects in data.yaml.

Usage:
    export GITHUB_TOKEN=ghp_xxx  # optional, higher rate limit
    python scripts/update_stars.py

Reads data.yaml, fetches current star counts for all github.com URLs,
and writes back with `stars` field updated. This is v0.1 of automation —
not run in CI yet, run manually before releases.
"""

import os
import re
import sys
import time
from pathlib import Path

try:
    import yaml
    import httpx
except ImportError:
    print("Install deps: pip install pyyaml httpx", file=sys.stderr)
    sys.exit(1)


REPO_URL_RE = re.compile(r"https?://github\.com/([^/]+)/([^/?#]+)")


def parse_repo(url: str) -> tuple[str, str] | None:
    m = REPO_URL_RE.match(url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    return owner, repo.rstrip("/").removesuffix(".git")


def fetch_stars(client: httpx.Client, owner: str, repo: str) -> int | None:
    resp = client.get(f"https://api.github.com/repos/{owner}/{repo}")
    if resp.status_code == 200:
        return resp.json().get("stargazers_count")
    if resp.status_code == 403:
        print(f"  rate-limited on {owner}/{repo}, sleeping 60s", file=sys.stderr)
        time.sleep(60)
        return fetch_stars(client, owner, repo)
    print(f"  {owner}/{repo}: HTTP {resp.status_code}", file=sys.stderr)
    return None


def main() -> int:
    root = Path(__file__).parent.parent
    data_path = root / "data.yaml"
    data = yaml.safe_load(data_path.read_text())

    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    updated = 0
    with httpx.Client(headers=headers, timeout=15.0) as client:
        for project in data.get("projects", []):
            url = project.get("url", "")
            parsed = parse_repo(url)
            if not parsed:
                continue
            owner, repo = parsed
            stars = fetch_stars(client, owner, repo)
            if stars is not None:
                project["stars"] = stars
                updated += 1
                print(f"  {owner}/{repo}: {stars}")
            time.sleep(0.5)

    data_path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False))
    print(f"\nUpdated {updated} projects.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
