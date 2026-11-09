"""Refresh data/stats.json (stars, last push, creation date) for every repo in data/tools.yaml.

Usage: GITHUB_TOKEN=... python scripts/update_stats.py
Uses the GitHub search API in batches, so it stays within the rate limit.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BATCH = 6


def repos_from_data() -> list[str]:
    data = yaml.safe_load((ROOT / "data" / "tools.yaml").read_text(encoding="utf-8"))
    repos = [i["repo"] for c in data["categories"] for i in c["items"]]
    repos += [i["repo"] for i in data.get("related", [])]
    return list(dict.fromkeys(repos))


def search(query: str, token: str | None) -> dict:
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": query, "per_page": 20})
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "awesome-ai-drama-stats"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    path = ROOT / "data" / "stats.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    today = dt.date.today().isoformat()
    repos = repos_from_data()
    stats, missing = {}, []
    for i in range(0, len(repos), BATCH):
        chunk = repos[i:i + BATCH]
        found = {r["full_name"].lower(): r for r in search(" ".join(f"repo:{r}" for r in chunk), token).get("items", [])}
        for name in chunk:
            r = found.get(name.lower())
            if not r:
                missing.append(name)
                if name in old:
                    stats[name] = old[name]
                continue
            stats[name] = {
                "stars": r["stargazers_count"],
                "pushed": r["pushed_at"][:10],
                "created": r["created_at"][:10],
                "archived": r["archived"],
                "license": (r.get("license") or {}).get("spdx_id"),
                "fetched": today,
            }
        time.sleep(2.5)
    path.write_text(json.dumps(stats, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    archived = [k for k, v in stats.items() if v.get("archived")]
    print(f"updated {len(stats)} repos; not found: {missing or 'none'}; archived: {archived or 'none'}")


if __name__ == "__main__":
    main()
