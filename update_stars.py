#!/usr/bin/env python3
"""
Refresh GitHub metrics for projects in data.yaml.

Usage:
    export GITHUB_TOKEN=ghp_xxx      # optional, but strongly recommended
    python update_stars.py           # run from anywhere; paths resolve to this file
    python update_stars.py --check   # exit 1 if anything is stale, change nothing

Reads data.yaml, fetches current `stargazers_count`, `pushed_at` and `archived`
for every github.com URL, and writes the values back into `stars:`, `pushed:`
and `archived:` fields, plus `last_verified:` at the top of the file.

Edits are made line-by-line on the raw text so that the comments and ordering in
data.yaml survive. A yaml.safe_load/yaml.dump round-trip would silently delete
every comment in the file, which is why this does not use one.

Exit codes: 0 ok, 1 stale (with --check) or write failure, 2 fetch errors.

History: in v0.1 this script resolved data.yaml as
`Path(__file__).parent.parent / "data.yaml"` while living in the repository root,
so it looked one directory ABOVE the repository and could never find the file.
It had never been run — no `stars` field existed anywhere in v0.1 or v0.2.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install deps: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.yaml"
API = "https://api.github.com/repos/"
REPO_URL_RE = re.compile(r"^https?://github\.com/([^/\s]+)/([^/?#\s]+)")

NAME_RE = re.compile(r"^  - name:\s*(.+?)\s*$")
URL_RE = re.compile(r'^    url:\s*"?([^"\s]+)"?\s*$')
STARS_RE = re.compile(r"^(    stars:\s*)(.*)$")
PUSHED_RE = re.compile(r"^(    pushed:\s*)(.*)$")
ARCHIVED_RE = re.compile(r"^(    archived:\s*)(.*)$")
VERIFIED_RE = re.compile(r"^(last_verified:\s*)(.*)$")


def parse_repo(url: str) -> tuple[str, str] | None:
    m = REPO_URL_RE.match(url)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    repo = repo.rstrip("/")
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def fetch(owner: str, repo: str, headers: dict[str, str], tries: int = 3) -> dict | None:
    """Return the repo payload, following renames. None on a hard failure."""
    req = urllib.request.Request(f"{API}{owner}/{repo}", headers=headers)
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 307, 308):
                # GitHub returns a redirect for renamed repositories; urllib
                # surfaces it as an error for the API's JSON media type.
                loc = e.headers.get("Location")
                if loc:
                    req = urllib.request.Request(loc, headers=headers)
                    continue
            if e.code == 403 and attempt < tries - 1:
                reset = e.headers.get("X-RateLimit-Reset")
                wait = 60
                if reset and reset.isdigit():
                    wait = max(5, int(reset) - int(time.time()) + 2)
                print(f"    rate-limited, waiting {wait}s", file=sys.stderr)
                time.sleep(min(wait, 900))
                continue
            if e.code == 404:
                print(f"    {owner}/{repo}: 404 — moved or deleted", file=sys.stderr)
                return None
            print(f"    {owner}/{repo}: HTTP {e.code}", file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < tries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            print(f"    {owner}/{repo}: {e}", file=sys.stderr)
            return None
    return None


def blocks(lines: list[str]) -> list[tuple[int, int, str, str]]:
    """Yield (start, end, name, url) for each project block in the projects list."""
    found: list[tuple[int, int, str, str]] = []
    starts = [i for i, ln in enumerate(lines) if NAME_RE.match(ln)]
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        name = NAME_RE.match(lines[start]).group(1).strip('"')
        url = ""
        for ln in lines[start:end]:
            m = URL_RE.match(ln)
            if m:
                url = m.group(1)
                break
        found.append((start, end, name, url))
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report staleness and exit non-zero; write nothing")
    ap.add_argument("--delay", type=float, default=0.4,
                    help="seconds between API calls (default 0.4)")
    args = ap.parse_args()

    if not DATA_PATH.exists():
        print(f"data.yaml not found at {DATA_PATH}", file=sys.stderr)
        return 1

    text = DATA_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Validate before touching anything: a malformed file should fail loudly.
    try:
        yaml.safe_load(text)
    except yaml.YAMLError as e:
        print(f"data.yaml is not valid YAML, refusing to edit: {e}", file=sys.stderr)
        return 1

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "top-industrial-ai-agents/update_stars",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        print("No GITHUB_TOKEN set — 60 requests/hour. Export one for a real run.",
              file=sys.stderr)

    updated = renamed = failed = 0
    changes: list[str] = []

    for start, end, name, url in blocks(lines):
        parsed = parse_repo(url) if url else None
        if not parsed:
            continue
        owner, repo = parsed
        data = fetch(owner, repo, headers)
        time.sleep(args.delay)
        if data is None:
            failed += 1
            continue

        stars = data.get("stargazers_count")
        pushed = (data.get("pushed_at") or "")[:10]
        archived = bool(data.get("archived"))
        full = data.get("full_name", f"{owner}/{repo}")

        if full.lower() != f"{owner}/{repo}".lower():
            renamed += 1
            changes.append(f"  RENAMED  {owner}/{repo} -> {full}  (update the url by hand)")

        have_stars = have_pushed = have_archived = False
        for i in range(start, end):
            m = STARS_RE.match(lines[i])
            if m:
                have_stars = True
                if m.group(2).strip() != str(stars):
                    changes.append(f"  {full}: stars {m.group(2).strip()} -> {stars}")
                lines[i] = f"{m.group(1)}{stars}"
                continue
            m = PUSHED_RE.match(lines[i])
            if m:
                have_pushed = True
                if m.group(2).strip() != pushed:
                    changes.append(f"  {full}: pushed {m.group(2).strip()} -> {pushed}")
                lines[i] = f"{m.group(1)}{pushed}"
                continue
            m = ARCHIVED_RE.match(lines[i])
            if m:
                have_archived = True
                was = m.group(2).strip()
                now = "true" if archived else "false"
                if was != now:
                    changes.append(f"  {full}: archived {was} -> {now}"
                                   + ("  <-- NOW ARCHIVED, review the entry" if archived else ""))
                lines[i] = f"{m.group(1)}{now}"

        # Insert any missing fields immediately after the url line.
        missing = []
        if not have_stars:
            missing.append(f"    stars: {stars}")
        if not have_pushed:
            missing.append(f"    pushed: {pushed}")
        if not have_archived:
            missing.append(f"    archived: {'true' if archived else 'false'}")
        if missing:
            for i in range(start, end):
                if URL_RE.match(lines[i]):
                    lines[i + 1:i + 1] = missing
                    changes.append(f"  {full}: added {len(missing)} missing field(s)")
                    break

        updated += 1
        print(f"  {full}: {stars} stars, pushed {pushed}"
              + (", ARCHIVED" if archived else ""))

    today = date.today().isoformat()
    for i, ln in enumerate(lines):
        m = VERIFIED_RE.match(ln)
        if m:
            lines[i] = f"{m.group(1)}{today}"
            break

    new_text = "\n".join(lines) + "\n"

    print(f"\nChecked {updated} repositories ({failed} failed, {renamed} renamed).")
    if changes:
        print("Changes:")
        for c in changes:
            print(c)

    if args.check:
        if new_text != text:
            print("\ndata.yaml is STALE — run without --check to refresh.", file=sys.stderr)
            return 1
        print("\ndata.yaml is up to date.")
        return 0

    if new_text == text:
        print("\nNothing to write; data.yaml already current.")
    else:
        DATA_PATH.write_text(new_text, encoding="utf-8")
        print(f"\nWrote {DATA_PATH}")

    try:
        yaml.safe_load(new_text)
    except yaml.YAMLError as e:
        print(f"WARNING: output is not valid YAML: {e}", file=sys.stderr)
        return 1

    if failed:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
